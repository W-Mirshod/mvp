from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connection as db_connection
from django.db.models import Q
from django.template import Context, Template
from django.utils import timezone
from email.utils import make_msgid
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from apps.backend_mailer.crud.crud_email import CRUDEmail
from apps.backend_mailer.crud.crud_sent_messages import CRUDSentMessages
from apps.backend_mailer.lockfile import default_lockfile, FileLock, FileLocked
from apps.backend_mailer.logutils import setup_loghandlers
from apps.backend_mailer.models import Email, EmailTemplate, Log, SentMessages
from apps.backend_mailer.settings import (
    get_batch_delivery_timeout,
    get_batch_size,
    get_log_level,
    get_max_retries,
    get_message_id_enabled,
    get_message_id_fqdn,
    get_retry_timedelta,
    get_sending_order,
    get_threads_per_process,
)
from apps.backend_mailer.signals import email_queued
from apps.backend_mailer.utils import (
    create_attachments,
    get_email_template,
    parse_emails,
    parse_priority,
    split_emails,
)
from apps.backend_mailer.constants import BackendConstants
from apps.mailers.constants import CampaignConstants
from apps.mailers.crud.crud_campaign import CRUDCampaign
from apps.notify.constants import NotifyConstants
from apps.notify.logic.general_user_notify import GeneralUserNotify

logger = setup_loghandlers("INFO")


def create(
    sender,
    recipients=None,
    cc=None,
    bcc=None,
    subject="",
    message="",
    html_message="",
    context=None,
    scheduled_time=None,
    expires_at=None,
    headers=None,
    template=None,
    priority=None,
    render_on_delivery=False,
    commit=True,
    email_backend=None,
):
    """
    Creates an email from supplied keyword arguments. If template is
    specified, email subject and content will be rendered during delivery.
    """
    priority = parse_priority(priority)
    status = (
        None
        if priority == BackendConstants.PRIORITY.now
        else BackendConstants.STATUS.queued
    )

    if recipients is None:
        recipients = []
    if cc is None:
        cc = []
    if bcc is None:
        bcc = []
    if context is None:
        context = ""
    message_id = (
        make_msgid(domain=get_message_id_fqdn()) if get_message_id_enabled() else None
    )

    # If email is to be rendered during delivery, save all necessary
    # information

    if render_on_delivery:
        email = Email(
            from_email=sender,
            to=recipients,
            cc=cc,
            bcc=bcc,
            scheduled_time=scheduled_time,
            expires_at=expires_at,
            message_id=message_id,
            headers=headers,
            priority=priority,
            status=status,
            context=context,
            template=template,
            email_backend=email_backend,
        )

    else:
        if template:
            subject = template.subject
            message = template.content
            html_message = template.html_content

        _context = Context(context or {})
        subject = Template(subject).render(_context)
        message = Template(message).render(_context)
        html_message = Template(html_message).render(_context)

        email = Email(
            from_email=sender,
            to=recipients,
            cc=cc,
            bcc=bcc,
            subject=subject,
            message=message,
            html_message=html_message,
            scheduled_time=scheduled_time,
            expires_at=expires_at,
            message_id=message_id,
            headers=headers,
            priority=priority,
            status=status,
            email_backend=email_backend,
            template=template,
        )

    if commit:
        email.save()

    return email


def send(
    recipients=None,
    sender=None,
    template=None,
    context=None,
    subject="",
    message="",
    html_message="",
    scheduled_time=None,
    expires_at=None,
    headers=None,
    priority=None,
    attachments=None,
    render_on_delivery=False,
    log_level=None,
    commit=True,
    cc=None,
    bcc=None,
    language="",
    email_backend=None,
):
    try:
        recipients = parse_emails(recipients)
    except ValidationError as e:
        raise ValidationError("recipients: %s" % e.message)

    try:
        cc = parse_emails(cc)
    except ValidationError as e:
        raise ValidationError("c: %s" % e.message)

    try:
        bcc = parse_emails(bcc)
    except ValidationError as e:
        raise ValidationError("bcc: %s" % e.message)

    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL

    priority = parse_priority(priority)

    if log_level is None:
        log_level = get_log_level()

    if not commit:
        if priority == BackendConstants.PRIORITY.now:
            raise ValueError("send_many() can't be used with priority = 'now'")
        if attachments:
            raise ValueError("Can't add attachments with send_many()")

    if template:
        if subject:
            raise ValueError(
                'You can\'t specify both "template" and "subject" arguments'
            )
        if message:
            raise ValueError(
                'You can\'t specify both "template" and "message" arguments'
            )
        if html_message:
            raise ValueError(
                'You can\'t specify both "template" and "html_message" arguments'
            )

        # template can be an EmailTemplate instance or name
        if isinstance(template, EmailTemplate):
            template = template
            # If language is specified, ensure template uses the right language
            if language and template.language != language:
                template = template.translated_templates.get(language=language)
        else:
            template = get_email_template(template, language)

    email = create(
        sender,
        recipients,
        cc,
        bcc,
        subject,
        message,
        html_message,
        context,
        scheduled_time,
        expires_at,
        headers,
        template,
        priority,
        render_on_delivery,
        commit=commit,
        email_backend=email_backend,
    )

    if attachments:
        attachments = create_attachments(attachments)
        email.attachments.add(*attachments)

    if priority == BackendConstants.PRIORITY.now:
        email.dispatch(log_level=log_level)
    elif commit:
        email_queued.send(sender=Email, emails=[email])

    return email


def send_many(kwargs_list, **kwargs):
    """
    Similar to mail.send(), but this function accepts a list of kwargs.
    Internally, it uses Django's bulk_create command for efficiency reasons.
    Currently send_many() can't be used to send emails with priority = 'now'.
    """
    emails = [send(commit=False, **kwargs) for kwargs in kwargs_list]
    if emails:
        CRUDEmail.bulk_email_create(create_objects=emails)
        email_queued.send(sender=Email, emails=emails)

    return emails


def get_queued():
    """
    Returns the queryset of emails eligible for sending – fulfilling these conditions:
     - Status is queued or requeued
     - Has scheduled_time before the current time or is None
     - Has expires_at after the current time or is None
    """
    now = timezone.now()
    query = (Q(scheduled_time__lte=now) | Q(scheduled_time=None)) & (
        Q(expires_at__gt=now) | Q(expires_at=None)
    )
    return (
        Email.objects.filter(
            query,
            status__in=[
                BackendConstants.STATUS.queued,
                BackendConstants.STATUS.requeued,
            ],
        )
        .select_related("template")
        .order_by(*get_sending_order())
        .prefetch_related("attachments")[: get_batch_size()]
    )


def send_queued(processes=1, log_level=None):
    """
    Sends out all queued mails that has scheduled_time less than now or None
    """
    queued_emails = get_queued()
    total_sent, total_failed, total_requeued = 0, 0, 0

    emails = [
        email
        for email in (email.to or email.bcc for email in queued_emails)
        for email in email
    ]
    total_email = len(emails)

    if log_level is None:
        log_level = get_log_level()

    if queued_emails:
        # Don't use more processes than number of emails
        if total_email < processes:
            processes = total_email

        if processes == 1:
            total_sent, total_failed, total_requeued = _send_bulk(
                emails=queued_emails,
                uses_multiprocessing=False,
                log_level=log_level,
            )
        else:
            email_lists = split_emails(queued_emails, processes)

            pool = Pool(processes)

            tasks = []
            for email_list in email_lists:
                tasks.append(pool.apply_async(_send_bulk, args=(email_list,)))

            timeout = get_batch_delivery_timeout()
            results = []

            # Wait for all tasks to complete with a timeout
            # The get method is used with a timeout to wait for each result
            for task in tasks:
                results.append(task.get(timeout=timeout))

            pool.terminate()
            pool.join()

            total_sent = sum(result[0] for result in results)
            total_failed = sum(result[1] for result in results)
            total_requeued = [result[2] for result in results]

    logger.info(
        "%s emails attempted, %s sent, %s failed, %s requeued",
        total_email,
        total_sent,
        total_failed,
        total_requeued,
    )

    return total_sent, total_failed, total_requeued


def _send_bulk(emails, uses_multiprocessing=True, log_level=None):
    # Multiprocessing does not play well with database connection
    # Fix: Close connections on forking process
    # https://groups.google.com/forum/#!topic/django-users/eCAIY9DAfG0
    if uses_multiprocessing:
        db_connection.close()

    if log_level is None:
        log_level = get_log_level()

    sent_emails = []
    failed_emails = []
    emails_list = [
        email
        for email in (email.to or email.bcc for email in emails)
        for email in email
    ]
    email_count = len(emails_list)

    logger.info("Process started, sending %s emails" % email_count)

    def send(email_obj, email_list):
        try:
            email_obj.dispatch(
                log_level=log_level, commit=False, disconnect_after_delivery=False
            )
            sent_emails.append(email_list)
            logger.debug("Successfully sent email #%d" % email.id)
        except Exception as e:
            logger.exception("Failed to send email #%d" % email.id)
            failed_emails.append((email, e))

    # Prepare emails before we send these to threads for sending
    # So we don't need to access the DB from within threads
    st_emails = []

    for email in emails:
        # Sometimes this can fail, for example when trying to render
        # email from a faulty Django template
        try:
            email.prepare_email_message()
        except Exception as e:
            logger.exception("Failed to prepare email #%d" % email.id)
            failed_emails.append((email, e))

    number_of_threads = min(get_threads_per_process(), email_count)
    pool = ThreadPool(number_of_threads)

    results = []
    for email in emails:
        for e in emails_list:
            st_emails.append(SentMessages(email=email, to=e))
        results.append(pool.apply_async(send, args=(email, emails_list)))

    if st_emails:
        CRUDSentMessages.bulk_sent_messages_create(st_emails)
    timeout = get_batch_delivery_timeout()

    # Wait for all tasks to complete with a timeout
    # The get method is used with a timeout to wait for each result
    for result in results:
        result.get(timeout=timeout)

    pool.close()
    pool.join()

    # Update statuses of sent emails

    email_ids = [email.id for email in emails]
    email_update = CRUDEmail.update_status(
        object_id=email_ids, status=BackendConstants.STATUS.sent
    )
    sent_message_update = CRUDSentMessages.update_status(
        object_id=email_ids, status=BackendConstants.STATUS.sent
    )

    logger.info(f"Successfully update {email_update} emails")
    logger.info(f"Successfully update {sent_message_update} sent messages")

    campaign_update = CRUDCampaign.update_campaign_status(
        object_id=email_ids, status=CampaignConstants.STATUS.completed
    )
    logger.info(f"Successfully update {campaign_update} campaigns")

    # Update statuses and conditionally requeue failed emails
    num_failed, num_requeued = 0, 0
    max_retries = get_max_retries()
    scheduled_time = timezone.now() + get_retry_timedelta()
    emails_failed = [email for email, _ in failed_emails]

    for email in emails_failed:
        if email.number_of_retries is None:
            email.number_of_retries = 0
        if email.number_of_retries < max_retries:
            email.number_of_retries += 1
            email.status = BackendConstants.STATUS.requeued
            email.scheduled_time = scheduled_time
            num_requeued += 1
        else:
            email.status = BackendConstants.STATUS.failed
            num_failed += 1
    CRUDEmail.bulk_email_update(update_objects=emails_failed)

    # If log level is 0, log nothing, 1 logs only sending failures
    # and 2 means log both successes and failures
    if log_level >= 1:
        logs = []
        for email, exception in failed_emails:
            logs.append(
                Log(
                    email=email,
                    status=BackendConstants.STATUS.failed,
                    message=str(exception),
                    exception_type=type(exception).__name__,
                )
            )

        if logs:
            Log.objects.bulk_create(logs)

    if log_level == 2:
        logs = []
        for email in emails:
            logs.append(Log(email=email, status=BackendConstants.STATUS.sent))

        if logs:
            Log.objects.bulk_create(logs)

    logger.info(
        "Process finished, %s attempted, %s sent, %s failed, %s requeued",
        email_count,
        len(sent_emails[0]),
        num_failed,
        num_requeued,
    )
    GeneralUserNotify.notify(
        user_id=str(emails[0].author.id),
        title=NotifyConstants.NOTIFICATION_SENT_MESSAGE_TITLE,
        description=NotifyConstants.NOTIFICATION_SENT_MESSAGE_DES
        % (
            email_count,
            len(sent_emails[0]),
            num_failed,
            num_requeued,
        ),
        notify_type=NotifyConstants.NOTIFICATIONS.item,
        data={
            "send_email": str(len(sent_emails[0])),
            "num_failed": num_failed,
            "num_requeued": num_requeued,
        },
    )
    return len(sent_emails[0]), num_failed, num_requeued


def send_queued_mail_until_done(lockfile=default_lockfile, processes=1, log_level=None):
    """
    Send mail in queue batch by batch, until all emails have been processed.
    """
    try:
        with FileLock(lockfile):
            logger.info("Acquired lock for sending queued emails at %s.lock", lockfile)
            while True:
                try:
                    send_queued(processes, log_level)
                except Exception as e:
                    logger.exception(e, extra={"status_code": 500})
                    raise

                # Close DB connection to avoid multiprocessing errors
                db_connection.close()

                if not get_queued().exists():
                    break
    except FileLocked:
        logger.info("Failed to acquire lock, terminating now.")
