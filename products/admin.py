from django.contrib import admin

from products.models import ProductModel


# Register your models here.
@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    ...