from rest_framework import serializers, status
from rest_framework.response import Response


# noinspection PyPep8Naming
def EMPTY_RESPONSE():
    return Response(status=status.HTTP_204_NO_CONTENT)


# noinspection PyAbstractClass
class EmptySerializer(serializers.Serializer):
    pass
