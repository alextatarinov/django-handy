from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin


class HiddenAttributesModel:
    """Raise AttributeError when accessing hidden_attributes"""
    hidden_attributes = []

    def __getattribute__(self, name):
        if name in super().__getattribute__('hidden_attributes'):
            raise AttributeError(name)
        return super().__getattribute__(name)


class PutModelMixin(HiddenAttributesModel, UpdateModelMixin):
    hidden_attributes = ['partial_update']


class PatchModelMixin(HiddenAttributesModel, UpdateModelMixin):
    hidden_attributes = ['update']


class UpdateViaCreateMixin(HiddenAttributesModel, UpdateModelMixin):
    """
        Update model instance via POST.

        This can be used in cases when only one model instance exists - i.e. user profile.
        Using just UpdateModelMixin is not suitable, because it requires to pass object pk.
    """
    hidden_attributes = ['partial_update', 'update']

    def create(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class RetrieveViaListMixin(HiddenAttributesModel, RetrieveModelMixin):
    """
       Retrieve model instance via GET.

       This can be used in cases when only one model instance exists - i.e. user profile.
       Using just RetrieveModelMixin is not suitable, because it requires to pass object pk.
    """
    hidden_attributes = ['retrieve']

    def list(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# noinspection PyUnresolvedReferences
class SerializerRequestMixin:
    @property
    def request(self):
        return self.context['request']
