from django import forms
from .models import QuizRating

class QuizRatingForm(forms.ModelForm):
    class Meta:
        model = QuizRating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'list-none'}),
        }

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'list-none'}),
    )