from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator:

    def __init__(self, message=None, code=None):
        self.message = message or 'Phone number must contain only digits.'
        self.code = code or 'Invalid phone number.'

    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError(self.message, code=self.code)
