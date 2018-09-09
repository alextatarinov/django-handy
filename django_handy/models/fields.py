from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from django_handy.helpers import unique_ordered


class PositiveDecimalField(models.DecimalField):
    default_validators = [MinValueValidator(0)]


class UniqueArrayField(ArrayField):
    """Ensures that no duplicates are saved to database"""

    def get_db_prep_value(self, value, connection, prepared=False):
        if isinstance(value, (list, tuple)):
            value = unique_ordered(value)
        return super().get_db_prep_value(value, connection, prepared)
