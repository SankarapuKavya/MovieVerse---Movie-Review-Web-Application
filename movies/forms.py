from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie

        fields = [
            'title',
            'description',
            'release_year',
            'genre',
            'poster',
            'trailer_url',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter movie title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter movie description'
                }
            ),

            'release_year': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'genre': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'poster': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'trailer_url': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://youtube.com/...'
                }
            ),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment',
        ]

        widgets = {
            'rating': forms.Select(
                choices=[
                    (1, '⭐ 1'),
                    (2, '⭐ 2'),
                    (3, '⭐ 3'),
                    (4, '⭐ 4'),
                    (5, '⭐ 5'),
                ],
                attrs={
                    'class': 'form-select'
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write your review...'
                }
            ),
        }