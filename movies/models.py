from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.PositiveIntegerField()

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='movies'
    )

    poster = models.ImageField(
        upload_to='movie_posters/',
        blank=True,
        null=True
    )

    trailer_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        reviews = self.reviews.all()

        if not reviews:
            return 0

        total = sum(review.rating for review in reviews)

        return round(total / len(reviews), 1)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'movie'],
                name='one_review_per_user_per_movie'
            )
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.user.username}"