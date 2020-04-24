try:
    from django.contrib.postgres.fields import ArrayField
except ImportError:
    ArrayField = None

from django import forms
from django.core.validators import MinValueValidator
from django.db import models

from django_handy.unique import unique_ordered
from django_handy.validation import MinValueExclusionValidator


class DefaultDecimalField(models.DecimalField):
    def __init__(self, max_digits=15, decimal_places=2, **kwargs):
        super().__init__(max_digits=max_digits, decimal_places=decimal_places, **kwargs)


class PositiveDecimalField(DefaultDecimalField):
    default_validators = [MinValueValidator(0)]

    def __init__(self, no_zero=False, **kwargs):
        if no_zero:
            validators = kwargs.pop('validators', [])
            validators.append(MinValueExclusionValidator(0))
            kwargs['validators'] = validators
        super().__init__(**kwargs)


if ArrayField:
    class UniqueArrayField(ArrayField):
        """Ensures that no duplicates are saved to database"""

        def get_db_prep_value(self, value, connection, prepared=False):
            if isinstance(value, (list, tuple)):
                value = unique_ordered(value)
            return super().get_db_prep_value(value, connection, prepared)


    class ChoicesUniqueArrayField(UniqueArrayField):
        def formfield(self, **kwargs):
            defaults = {
                'form_class': forms.MultipleChoiceField,
                'choices': self.base_field.choices,
                'widget': forms.CheckboxSelectMultiple,
            }
            defaults.update(kwargs)
            # This super() call is intentional to jump over ArrayField.formfield
            return super(ArrayField, self).formfield(**defaults)
