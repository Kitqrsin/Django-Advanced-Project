from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class ChamillionUser(AbstractUser):
    phone_number = PhoneNumberField(
        blank=True,
        help_text='Contact phone number'
    )