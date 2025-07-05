from django.db import models

from reviews.choices import StarRatingChoices


class ReviewModel(models.Model):
    product = models.ForeignKey(
        'products.ProductModel',
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )

    account = models.ForeignKey(
        'accounts.AccountModel',
        on_delete=models.CASCADE,
        related_name = 'account_reviews'
    )

    comment = models.TextField(

    )

    star_rating = models.CharField(
        choices=StarRatingChoices.choices,
        default=StarRatingChoices.CHOOSE_RATING
    )