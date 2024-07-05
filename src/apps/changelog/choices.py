from enum import Enum


class ActionType(Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]
