from django.db.models import DecimalField, Func


class Round(Func):
    function = 'ROUND'
    _output_field = DecimalField()

    def __init__(self, expression, places=2, **extra):
        super().__init__(expression, places, **extra)
