from django import forms
from .models import ReviewModel

class AddReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ('comment', 'star_rating')