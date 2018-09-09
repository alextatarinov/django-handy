import mimetypes
from decimal import Decimal
from functools import wraps
from typing import Dict, List

import collections
from django.db import models, transaction
from django.http import HttpResponse
from django.utils.encoding import force_text


def create_attachment_response(filename, content: bytes):
    """
        Creates response to download file with correct headers
         for given content and filename
    """
    response = HttpResponse(content=content)
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    mime_type, encoding = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'
    response['Content-Type'] = mime_type

    response['Access-Control-Expose-Headers'] = 'Content-Disposition'

    if encoding is not None:
        response['Content-Encoding'] = encoding

    return response


def simple_urljoin(*args):
    """
        Joins url parts like 'https://', 'google.com/', '/search/' to https://google.com/search/

        Treats parts ending on double slash as url beginning and ignores all parts before them.
        Other parts are treated as path and joined with single slash.

        Preserves single trailing and leading slash.
    """
    sep = '/'
    res = ''

    for idx, piece in enumerate(args):
        is_first = idx == 0
        is_last = idx == len(args) - 1

        add_leading_slash = add_trailing_slash = False

        piece = force_text(piece)

        if is_first and piece.startswith(sep):
            add_leading_slash = True

        if is_last and piece.endswith(sep):
            add_trailing_slash = True

        if not is_last:
            add_trailing_slash = True

        piece = piece.strip('/')

        if '://' in piece:
            res = piece

        if add_leading_slash:
            res = sep + res

        if add_trailing_slash:
            res += sep

    return res


def get_attribute(instance, name):
    """
    Similar to Python's built in `getattr(instance, attr)`,
    but takes a list of nested attributes, instead of a single attribute.

    Also accepts either attribute lookup on objects or dictionary lookups.
    """

    attrs = name.split('.')
    for attr in attrs:
        if isinstance(instance, collections.Mapping):
            try:
                instance = instance[attr]
            except KeyError as exc:
                raise AttributeError(exc) from exc
        else:
            instance = getattr(instance, attr)
    return instance


def has_attribute(obj, name):
    """
        Like normal hasattr, but follows dotted paths
    """
    try:
        get_attribute(obj, name)
    except AttributeError:
        return False

    return True


def bulk_dict_update(dicts_list: List[Dict], update_dict: Dict):
    for dict_ in dicts_list:
        dict_.update(update_dict)


def is_empty(val):
    if val is None or val == '' or val == []:
        return True
    return False


def all_not_empty(obj, *attrs):
    return all(not is_empty(get_attribute(obj, field)) for field in attrs)


def any_not_empty(obj, *attrs):
    return any(not is_empty(get_attribute(obj, field)) for field in attrs)


def join_not_empty(separator, *args):
    return separator.join(arg for arg in args if not is_empty(arg))


def unique_ordered(seq):
    seen = set()
    unique = []
    for x in seq:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    return unique


class UpdateDict(dict):
    def __init__(self, update_data, instance):
        super().__init__()
        self.update_data = update_data
        self.instance = instance

    def __getitem__(self, item):
        if item in self.update_data:
            return self.update_data[item]
        return getattr(self.instance, item)

    def get(self, item, default=None):
        try:
            return self[item]
        except AttributeError:
            return default


def get_unique_objs(objs: List[models.Model], unique_fields: List[str]) -> List[models.Model]:
    seen_obj_footprints = set()
    unique_objs = []
    for obj in objs:
        obj_footprint = tuple(getattr(obj, field) for field in unique_fields)
        if obj_footprint in seen_obj_footprints:
            continue

        seen_obj_footprints.add(obj_footprint)
        unique_objs.append(obj)
    return unique_objs


def d_round(value, places=2):
    assert isinstance(places, int)
    quantize_to = Decimal(10) ** (-places)
    return Decimal(value).quantize(quantize_to)


def call_on_commit(func):
    """
    Only call the decorated function at transaction commit.
    The return value will be ignored
    """

    @wraps(func)
    def handle(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return handle
