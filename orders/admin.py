from django.contrib import admin

from orders.models import OrderModel


# Register your models here.
@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    ...