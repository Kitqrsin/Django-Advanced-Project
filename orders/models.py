from django.core.validators import MinValueValidator
from django.db import models
from orders.choices import StatusChoices, DeliveryChoices


class OrderModel(models.Model):
    account = models.ForeignKey(
        'accounts.ChamillionUser',
        on_delete=models.CASCADE,
        related_name='account_orders',
        null=True,
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
        max_length=15,
        default=StatusChoices.PENDING
    )

    first_name = models.CharField(
        max_length=50,
        blank=True
    )

    last_name = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    region = models.CharField(max_length=100)

    city = models.CharField(
        max_length=100,
        default='Sofia'
    )

    country = models.CharField(
        max_length=100,
        default='България'
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    address_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryChoices.choices
    )

    econt_office_address = models.CharField(
        max_length=255,
        null=True,
    )

    def __str__(self):
        return f'Order #{self.id} - {self.account}'


class OrderItemsModel(models.Model):
    orders = models.ForeignKey(
        'OrderModel',
        on_delete=models.CASCADE,
        related_name='order_items'
    )

    items = models.ForeignKey(
        'products.ProductModel',
        on_delete=models.CASCADE,
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
