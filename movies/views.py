from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

from .models import Movie, Genre, Review
from .forms import MovieForm, ReviewForm

def home(request):
    movies = Movie.objects.all().order_by('-created_at')[:6]

    return render(
        request,
        'movies/home.html',
        {
            'movies': movies
        }
    )
def movie_list(request):

    movies = Movie.objects.all()
    genres = Genre.objects.all()

    search_query = request.GET.get('q')
    genre_id = request.GET.get('genre')

    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if genre_id:
        movies = movies.filter(genre_id=genre_id)

    return render(
        request,
        'movies/movie_list.html',
        {
            'movies': movies,
            'genres': genres,
            'search_query': search_query,
            'selected_genre': genre_id,
        }
    )
def movie_detail(request, pk):

    movie = get_object_or_404(
        Movie,
        pk=pk
    )

    reviews = movie.reviews.select_related(
        'user'
    ).all()

    review_form = ReviewForm()

    return render(
        request,
        'movies/movie_detail.html',
        {
            'movie': movie,
            'reviews': reviews,
            'review_form': review_form,
        }
    )
@login_required
def add_review(request, pk):

    movie = get_object_or_404(
        Movie,
        pk=pk
    )

    if request.method == 'POST':

        form = ReviewForm(request.POST)

        if form.is_valid():

            existing_review = Review.objects.filter(
                movie=movie,
                user=request.user
            ).first()

            if existing_review:
                messages.warning(
                    request,
                    'You have already reviewed this movie.'
                )

                return redirect(
                    'movie_detail',
                    pk=movie.pk
                )

            review = form.save(commit=False)

            review.movie = movie
            review.user = request.user

            review.save()

            messages.success(
                request,
                'Your review was added successfully!'
            )

    return redirect(
        'movie_detail',
        pk=movie.pk
    )
@staff_member_required
def movie_create(request):

    if request.method == 'POST':

        form = MovieForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Movie added successfully!'
            )

            return redirect('movie_list')

    else:

        form = MovieForm()

    return render(
        request,
        'movies/movie_form.html',
        {
            'form': form,
            'page_title': 'Add Movie'
        }
    )
@staff_member_required
def movie_update(request, pk):

    movie = get_object_or_404(
        Movie,
        pk=pk
    )

    if request.method == 'POST':

        form = MovieForm(
            request.POST,
            request.FILES,
            instance=movie
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Movie updated successfully!'
            )

            return redirect(
                'movie_detail',
                pk=movie.pk
            )

    else:

        form = MovieForm(
            instance=movie
        )

    return render(
        request,
        'movies/movie_form.html',
        {
            'form': form,
            'movie': movie,
            'page_title': 'Edit Movie'
        }
    )
@staff_member_required
def movie_delete(request, pk):

    movie = get_object_or_404(
        Movie,
        pk=pk
    )

    if request.method == 'POST':

        movie.delete()

        messages.success(
            request,
            'Movie deleted successfully!'
        )

        return redirect('movie_list')

    return render(
        request,
        'movies/movie_confirm_delete.html',
        {
            'movie': movie
        }
    )