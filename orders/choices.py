from django.db import models


class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    PAID = 'paid', 'Paid'
    CANCELLED = 'cancelled', 'Cancelled'