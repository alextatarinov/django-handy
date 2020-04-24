from rest_framework.mixins import UpdateModelMixin


class PutModelMixin(UpdateModelMixin):
    def __getattribute__(self, name):
        if name == 'update':
            raise AttributeError(name)
        return super().__getattribute__(name)
