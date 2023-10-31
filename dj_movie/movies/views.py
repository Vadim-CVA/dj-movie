from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.shortcuts import redirect, render
from .models import Movie, Actor, Genre
from .forms import ReviewForm
from django.db.models.query import Q


class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()
    
    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear,ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    

class MovieDetailView(GenreYear,DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = "url"


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
    

class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""

    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    def get_queryset(self):
        my_q = Q()
        if 'year' in self.request.GET:
            my_q = Q(year__in=self.request.GET.getlist('year'))
        if 'genres' in self.request.GET:
            my_q &= Q(genre__in=self.request.GET.getlist('genres'))
        queryset = Movie.objects.filter(my_q)
        return queryset
    
    




