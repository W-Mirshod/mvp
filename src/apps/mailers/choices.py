from django.utils.translation import gettext_lazy as _


class StatusType:
    """
    Type of the status mailer
    """

    NEW = "new"
    FINISHED = "finished"
    IN_PROCESS = "in_process"
    FAILED = "failed"
    CANCELED = "canceled"

    ITEMS = [NEW, FINISHED, IN_PROCESS, FAILED, CANCELED]

    CHOICES = (
        (NEW, _("New")),
        (FINISHED, _("Finished")),
        (IN_PROCESS, _("In Process")),
        (FAILED, _("Failed")),
        (CANCELED, _("Canceled")),
    )
