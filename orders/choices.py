from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'


class DeliveryChoices(models.TextChoices):
    ECONT = 'econt', 'Econt'
    SAMEDAY_EASYBOX = 'sameday_easybox', 'Sameday Easybox',
    SAMEDAY_ADDRESS = 'sameday_address', 'Sameday to address'