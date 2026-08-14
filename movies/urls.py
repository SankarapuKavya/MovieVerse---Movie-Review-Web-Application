from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'movies/',
        views.movie_list,
        name='movie_list'
    ),

    path(
        'movies/<int:pk>/',
        views.movie_detail,
        name='movie_detail'
    ),

    path(
        'movies/add/',
        views.movie_create,
        name='movie_create'
    ),

    path(
        'movies/<int:pk>/edit/',
        views.movie_update,
        name='movie_update'
    ),

    path(
        'movies/<int:pk>/delete/',
        views.movie_delete,
        name='movie_delete'
    ),

    path(
        'movies/<int:pk>/review/',
        views.add_review,
        name='add_review'
    ),
]