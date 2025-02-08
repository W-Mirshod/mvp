from django.utils.translation import gettext_lazy as _

class TaskStatus:
    """Task processing status choices"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

    CHOICES = (
        (PENDING, _("Pending")),
        (IN_PROGRESS, _("In Progress")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
    )

    ITEMS = [PENDING, IN_PROGRESS, COMPLETED, FAILED]


class TaskResult:
    """Task result status choices"""

    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"

    CHOICES = (
        (SUCCESS, _("Success")),
        (FAILURE, _("Failure")),
        (TIMEOUT, _("Timeout")),
    )

    ITEMS = [SUCCESS, FAILURE, TIMEOUT]
