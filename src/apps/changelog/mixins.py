from django.db import models


class ChangeloggableMixin(models.Model):
    """Field values immediately after object initialization"""

    _original_values = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ChangeloggableMixin, self).__init__(*args, **kwargs)

        self._original_values = {}
        for field in self._meta.fields:
            if isinstance(field, models.ForeignKey):
                self._original_values[field.name] = getattr(self, f"{field.name}_id")
            else:
                self._original_values[field.name] = getattr(self, field.name)

    def get_changed_fields(self):
        """Receiving the changed data"""
        result = {}
        for name, original_value in self._original_values.items():
            current_value = getattr(self, name)
            if original_value != current_value:
                if isinstance(self._meta.get_field(name), models.ForeignKey):
                    if original_value != getattr(self, f"{name}_id"):
                        result[name] = current_value
                else:
                    result[name] = current_value
        return result
