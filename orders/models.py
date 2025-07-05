from django.core.validators import MinValueValidator
from django.db import models

from orders.choices import StatusChoices


class OrderModel(models.Model):
    account = models.ForeignKey(
        'accounts.ChamillionUser',
        on_delete=models.CASCADE,
        related_name='account_orders'
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    status = models.CharField(
        choices=StatusChoices.choices,
        max_length=15
    )

class OrderItemsModel(models.Model):
    orders = models.ForeignKey(
        'OrderModel',
        on_delete= models.CASCADE,
        related_name='order_items'
    )


    items = models.ForeignKey(
        'products.ProductModel',
        on_delete= models.CASCADE,
        related_name='item_orders'
    )

    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )