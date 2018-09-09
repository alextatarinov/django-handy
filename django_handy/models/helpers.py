from typing import List, Type

from django.db import models
from manager_utils import bulk_upsert

from django_handy.helpers import get_unique_objs


def get_bulk_update_fields(cls: Type[models.Model], unique_fields: List[str] = None) -> List[str]:
    opts = cls._meta
    if unique_fields is None:
        unique_fields = get_unique_fields(cls)

    return [
        field.name for field in opts.get_fields()
        if (
            field.name not in unique_fields and
            not (field.many_to_many or field.one_to_many)
        )
    ]


def get_unique_fields(cls: Type[models.Model]) -> List[str]:
    opts = cls._meta
    if opts.unique_together:
        return opts.unique_together[0]
    raise ValueError(f'{cls}.Meta does not declare unique_together')


def is_editable(f: models.Field):
    return f.editable and not f.auto_created


def safe_bulk_upsert(
    queryset: models.QuerySet, model_objs: List[models.Model],
    unique_fields: List[str], update_fields: List[str] = None,
    return_upserts: bool = False, return_upserts_distinct: bool = False,
    sync: bool = False, native: bool = False
):
    """
    Removes objs with duplicate unique fields to prevent IntegrityError.
    Uses first unique obj encountered
    """
    # noinspection PyTypeChecker
    return bulk_upsert(
        queryset,
        model_objs=get_unique_objs(model_objs, unique_fields),
        unique_fields=unique_fields,
        update_fields=update_fields,
        return_upserts=return_upserts,
        return_upserts_distinct=return_upserts_distinct,
        sync=sync,
        native=native
    )
