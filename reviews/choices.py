from django.db import models


class StarRatingChoices(models.TextChoices):
    """
    ★★★★★ - Excellent
    ★★★★☆ - Good
    ★★★☆☆ - Average
    ★★☆☆☆ - Poor
    ★☆☆☆☆ - Terrible
    """

    EXCELLENT = '★★★★★', 'Excellent'
    GOOD = '★★★★☆', 'Good'
    AVERAGE = '★★★☆☆', 'Average'
    POOR = '★★☆☆☆', 'Poor'
    TERRIBLE = '★☆☆☆☆', 'Terrible'
    CHOOSE_RATING = "choose your rating...", "Choose your rating..."