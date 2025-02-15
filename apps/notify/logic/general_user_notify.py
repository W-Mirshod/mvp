import logging

from apps.notify.crud.crud_notification import CRUDNotification

logger = logging.getLogger(__name__)


class GeneralUserNotify:

    @staticmethod
    def notify(
        user_id: str,
        title: str,
        description: str,
        notify_type: int,
        data: dict[str, str],
    ) -> None:
        """tba"""

        logger.info(
            f"Create notification  : user={str(user_id)=}, user={str(user_id)=}, title={title=}, description={description=}, notify_type={notify_type=},  data={data=}"
        )

        CRUDNotification.create_notification(
            data={
                "user_id": str(user_id),
                "title": title,
                "description": description,
                "notify_type": notify_type,
                "data": data,
            }
        )
