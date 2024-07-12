from django.db import models
from django.db.models import fields


class ChangeloggableMixin(models.Model):
    """Field values immediately after object initialization"""

    _original_values = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ChangeloggableMixin, self).__init__(*args, **kwargs)

        self._original_values = {}
        for field in self._meta.fields:

            if type(field) == fields.related.ForeignKey:
                self._original_values[field.name] = getattr(self, f"{field.name}_id")

            else:
                self._original_values[field.name] = getattr(self, field.name)

    def get_changed_fields(self):
        """
        Getting the modified data
        """
        result = {}

        for name, value in self._original_values.items():

            if value != getattr(self, name):

                temp = {}
                temp[name] = getattr(self, name)

                # Additional validation for Foreign Key fields
                if self._meta.get_field(name).get_internal_type() == ("ForeignKey"):
                    if value != getattr(self, f"{name}_id"):
                        result.update(temp)

                # For the rest of the fields, we simply output the result
                else:
                    result.update(temp)

        return result
