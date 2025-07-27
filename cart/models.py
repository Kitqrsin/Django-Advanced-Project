from django.core.validators import MinValueValidator
from django.db import models

class CartModel(models.Model):
    account = models.OneToOneField(
        'accounts.ChamillionUser',
        on_delete=models.CASCADE,
        related_name='cart'
    )


class CartsProductsModel(models.Model):
    carts = models.ForeignKey(
        'CartModel',
        on_delete=models.CASCADE,
        related_name='cart_products',
    )

    products = models.ForeignKey(
        'products.ProductModel',
        on_delete=models.CASCADE,
        related_name='product_carts'
    )

    size = models.ForeignKey(
        'products.SizeModel',
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )

