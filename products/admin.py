from django.contrib import admin

from products.models import ProductModel, ProductSize, CategoryModel, SizeModel


# Register your models here.
class ProductSizeInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductSize
    extra = 1  # Number of empty forms to show
    min_num = 1  # Enforce at least one
    verbose_name = "Size & Quantity"
    verbose_name_plural = "Sizes & Quantities"


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'unit_price')
    inlines = [ProductSizeInline]
    filter_horizontal = ('categories',)  # Enables better multi-select widget


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(SizeModel)
class SizeModelAdmin(admin.ModelAdmin):
    list_display = ('size_name',)