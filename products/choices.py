from django.db import models


class CategoryChoices(models.TextChoices):
    MEN = "men", "Men"
    WOMEN = "women", "Women"
    CHILDREN = "children", "Children"
    ACCESSORIES = "accessories",  "Accessories"