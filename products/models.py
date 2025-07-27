from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

from products.choices import CategoryChoices, SizeChoices


class ProductModel(models.Model):
    product_name = models.CharField(
        max_length=50,
    )

    product_description = models.TextField(
        max_length=255,
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    product_image = models.ImageField(
        upload_to='products/'
    )

    categories = models.ManyToManyField(
        'CategoryModel',
        related_name='products',
    )

    sizes = models.ManyToManyField(
        'SizeModel',
        through='ProductSize',
        related_name='products'
    )

    @property
    def total_quantity(self):
        return sum(ps.quantity for ps in self.productsize_set.all())

    @property
    def is_available(self):
        return any(ps.quantity > 0 for ps in self.productsize_set.all())

    def clean(self):

        if self.pk:
            size_entries = self.productsize_set.all()
            if not size_entries.exists():
                raise ValidationError('Each product must have at least one size with quantity.')
            for entry in size_entries:
                if entry.quantity < 0:
                    raise ValidationError({'sizes': f"Size {entry.size.size_name} has negative quantity."})


    def get_average_rating(self):
        reviews = self.product_reviews.all()
        if not reviews.exists():
            return 0.0

        star_map = {
            '★★★★★': 5,
            '★★★★☆': 4,
            '★★★☆☆': 3,
            '★★☆☆☆': 2,
            '★☆☆☆☆': 1,
        }

        total = 0
        count = 0

        for review in reviews:
            stars = star_map.get(review.star_rating)
            if stars is not None:
                total += stars
                count += 1

        if count == 0:
            return 0.0

        return round(total / count, 1)

    def __str__(self):
        return self.product_name


class CategoryModel(models.Model):
    category_name = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        default=CategoryChoices.MEN,
    )

    def __str__(self):
        return self.get_category_name_display()


class SizeModel(models.Model):
    size_name = models.CharField(
        max_length=4,
        choices=SizeChoices.choices,
        default=SizeChoices.M,
    )

    def __str__(self):
        return self.size_name


class ProductSize(models.Model):
    product = models.ForeignKey(
        'ProductModel',
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        'SizeModel',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')
