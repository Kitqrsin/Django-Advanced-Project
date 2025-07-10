from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from products.choices import CategoryChoices


class ProductModel(models.Model):

    product_name = models.CharField(
        max_length=50,
    )

    product_description = models.TextField(
        max_length=255,
    )

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    available = models.BooleanField(
        default=True,
    )

    product_image = models.ImageField(
        upload_to='products/'
    )

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.available = False
        else:
            self.available = True
        super().save(*args, **kwargs)

    def clean(self):
        if self.quantity < 0:
            raise ValidationError({'quantity': 'Quantity cannot be negative!'})


class CategoryModel(models.Model):
    category_name = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.MEN,
    )
    product = models.ForeignKey(
        'ProductModel',
        on_delete=models.CASCADE,
        related_name='categories'
    )