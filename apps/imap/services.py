import imaplib
import email
import logging
from email.header import decode_header
from typing import Dict, List
from django.core.cache import cache
from datetime import datetime
from .exceptions import IMAPError

logger = logging.getLogger(__name__)

class IMAPService:
    CACHE_TIMEOUT = 300  # 5 minutes
    IMPORTANT_FOLDERS = ['INBOX', 'Spam', 'Junk']

    def __init__(self, account):
        self.account = account
        self.conn = None

    def _connect(self) -> None:
        try:
            self.conn = imaplib.IMAP4_SSL(
                host=self.account.imap_server,
                port=self.account.imap_port,
                timeout=10
            )
            self.conn.login(self.account.email, self.account.password)
        except Exception as e:
            raise IMAPError(f"Connection failed: {str(e)}")

    def _disconnect(self):
        if self.conn:
            self.conn.logout()
            self.conn = None

    def _parse_email(self, email_id: bytes, msg_data: tuple) -> Dict:
        email_message = email.message_from_bytes(msg_data[0][1])
        
        # Decode subject properly
        subject = decode_header(email_message.get('subject', ''))[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        # Parse date
        date_str = email_message.get('date')
        try:
            date = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            formatted_date = date.isoformat()
        except (ValueError, TypeError):
            formatted_date = date_str

        return {
            'id': email_id.decode(),
            'subject': subject or '(No Subject)',
            'from': email_message.get('from', ''),
            'date': formatted_date,
            'has_attachments': any(part.get_filename() for part in email_message.walk())
        }

    def check_folder(self, folder_name: str = 'INBOX') -> Dict:
        try:
            self._connect()
            self.conn.select(folder_name, readonly=True)
            total = len(self.conn.search(None, 'ALL')[1][0].split())
            unread = len(self.conn.search(None, 'UNSEEN')[1][0].split())
            return {'total': total, 'unread': unread}
        except Exception as e:
            logger.error(f"Error checking folder {folder_name}: {str(e)}")
            raise
        finally:
            self._disconnect()

    def get_latest_emails(self, folder_name: str = 'INBOX', limit: int = 5) -> List[Dict]:
        try:
            self._connect()
            self.conn.select(folder_name, readonly=True)
            status, messages = self.conn.search(None, 'ALL')
            if status != 'OK':
                raise IMAPError(f"Failed to search folder: {status}")
                
            email_ids = messages[0].split()
            if not email_ids:
                return []
                
            email_ids = email_ids[-limit:]
            results = []
            
            for email_id in reversed(email_ids):
                status, msg_data = self.conn.fetch(email_id, '(RFC822)')
                if status == 'OK' and msg_data and msg_data[0]:
                    results.append(self._parse_email(email_id, msg_data))
                    
            return results
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            raise IMAPError(f"Failed to fetch emails: {str(e)}")
        finally:
            self._disconnect()

    def get_folder_stats(self) -> Dict:
        cache_key = f"imap_stats_{self.account.email}"
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return cached_stats

        try:
            self._connect()
            stats = {}
            
            for folder in self.IMPORTANT_FOLDERS:
                try:
                    self.conn.select(folder, readonly=True)
                    total = len(self.conn.search(None, 'ALL')[1][0].split())
                    unread = len(self.conn.search(None, 'UNSEEN')[1][0].split())
                    stats[folder.lower()] = {
                        'total': total,
                        'unread': unread,
                        'updated_at': datetime.now().isoformat()
                    }
                except Exception as e:
                    logger.warning(f"Error checking folder {folder}: {str(e)}")
                    stats[folder.lower()] = {'total': 0, 'unread': 0, 'error': str(e)}

            cache.set(cache_key, stats, self.CACHE_TIMEOUT)
            return stats
        finally:
            self._disconnect()
