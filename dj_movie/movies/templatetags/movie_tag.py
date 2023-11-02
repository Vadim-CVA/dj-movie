from django import template
from movies.models import Category,Movie
from django.db.models import Avg

register = template.Library()

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=3):
    movies = Movie.objects.order_by("id").reverse()[:count]
    return {'last_movies': movies}