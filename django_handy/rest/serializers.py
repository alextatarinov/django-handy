import requests
from rest_framework import serializers


# noinspection PyAbstractClass
class EmptySerializer(serializers.Serializer):
    pass


# noinspection PyAbstractClass
class ReCaptchaSerializer(serializers.Serializer):
    SECRET = None
    recaptcha = serializers.CharField(write_only=True)

    def validate_recaptcha(self, recaptcha):
        data = {
            'secret': self.SECRET,
            'response': recaptcha
        }
        try:
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout=10)
            result = response.json()

            if not result['success']:
                raise serializers.ValidationError('reCAPTCHA is not valid')

        except requests.Timeout:
            pass

        # Do not add recaptcha to validated_data - it is useless
        raise serializers.SkipField
