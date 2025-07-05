from django.core.validators import MinLengthValidator
from django.db import models


class AccountModel(models.Model):


    first_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(3)
        ]
    )

    last_name = models.CharField(
        max_length=25,
        validators=[
            MinLengthValidator(3)
        ]
    )

    email = models.EmailField(

    )

    address = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(5)
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )
