from rest_framework.mixins import UpdateModelMixin


class HiddenAttributesMeta(type):
    """Raise AttributeError when accessing hidden_attributes on class itself"""

    def __getattribute__(self, name):
        if name in super().__getattribute__('hidden_attributes'):
            raise AttributeError(name)
        return super().__getattribute__(name)


class PutModelMixin(metaclass=HiddenAttributesMeta, UpdateModelMixin):
    hidden_attributes = ['partial_update']
