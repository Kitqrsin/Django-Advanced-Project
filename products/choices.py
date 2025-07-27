from django.db import models


class CategoryChoices(models.TextChoices):
    MEN = "men", "Men"
    WOMEN = "women", "Women"
    CHILDREN = "children", "Children"
    ACCESSORIES = "accessories",  "Accessories"


class SizeChoices(models.TextChoices):
    XS = 'XS', 'XS'
    S = 'S', 'S'
    M = 'M', 'M'
    L = 'L', 'L'
    XL = 'XL', 'XL'
    XXL = 'XXL', 'XXL'
