from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.shortcuts import redirect, render
from .models import Movie, Actor, Genre, Rating
from .forms import ReviewForm,RatingForm
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
    paginate_by = 9
    

class MovieDetailView(GenreYear,DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm() 
        return context
        


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

    template_name = "movies/movie_list.html"
    paginate_by = 3

    def get_queryset(self):
        my_q = Q()
        if 'year' in self.request.GET:
            my_q = Q(year__in=self.request.GET.getlist('year'))
        if 'genres' in self.request.GET:
            my_q &= Q(genres__in=self.request.GET.getlist('genres'))
        queryset = Movie.objects.filter(my_q).distinct()
        return queryset
        

class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        movie = Movie.objects.get(id=int(request.POST.get("movie")))
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return redirect(movie.get_absolute_url())
        else:
            return HttpResponse(status=400)
    
    
class Search(ListView):
    '''Поиск фильма'''
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'&q={self.request.GET.get("q")}'
        return context
    
