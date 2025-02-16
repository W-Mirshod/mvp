import csv
import io
import logging
from typing import List, Dict
from apps.mail_servers.models.mailer import Base, SMTP, Log, Proxy

logger = logging.getLogger(__name__)


class ExportService:
    @staticmethod
    def export_to_csv(data: List[Dict], fields: List[str]) -> str:
        """Export data to CSV format"""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    @staticmethod
    def export_bases(session: str) -> str:
        """Export email address base"""
        bases = Base.objects.filter(session=session).values("first", "last", "email")
        return ExportService.export_to_csv(bases, ["first", "last", "email"])

    @staticmethod
    def export_smtp(session: str) -> str:
        """Export SMTP servers"""
        smtps = SMTP.objects.filter(session=session).values(
            "server", "port", "email", "password", "status"
        )
        return ExportService.export_to_csv(
            smtps, ["server", "port", "email", "password", "status"]
        )

    @staticmethod
    def export_proxy(session: str) -> str:
        """Export proxies"""
        proxies = Proxy.objects.filter(session=session).values("ip", "port", "status")
        return ExportService.export_to_csv(proxies, ["ip", "port", "status"])

    @staticmethod
    def export_logs(session: str) -> str:
        """Export logs"""
        logs = Log.objects.filter(session=session).values(
            "created_at", "type", "text", "status"
        )
        return ExportService.export_to_csv(
            logs, ["created_at", "type", "text", "status"]
        )
