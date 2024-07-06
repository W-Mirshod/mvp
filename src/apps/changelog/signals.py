import json

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .choices import ActionType
from .middleware import get_current_url, get_current_user
from .mixins import ChangeloggableMixin
from .models import ChangeLog


@receiver(post_save)
def log_changes_on_save(sender, instance, created, **kwargs):
    if not isinstance(instance, ChangeloggableMixin) or sender == ChangeLog:
        return

    action = ActionType.CREATED.value if created else ActionType.UPDATED.value
    changes = instance.get_changed_fields()
    current_user = get_current_user()
    current_url = get_current_url()

    ChangeLog.objects.create(
        user=current_user,
        url=current_url,
        model_name=sender.__name__,
        object_id=instance.pk,
        data=json.dumps(changes),
        action=action,
    )


@receiver(pre_delete)
def log_changes_on_delete(sender, instance, **kwargs):
    if not isinstance(instance, ChangeloggableMixin) or sender == ChangeLog:
        return

    changes = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
    current_user = get_current_user()
    current_url = get_current_url()

    ChangeLog.objects.create(
        user=current_user,
        url=current_url,
        model_name=sender.__name__,
        object_id=instance.pk,
        data=json.dumps(changes),
        action=ActionType.DELETED.value,
    )
