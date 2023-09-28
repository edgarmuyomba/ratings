from django.urls import path 
from django.views.generic import TemplateView
from .views import search, details, episode_ratings

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name="core/index.html"), name='index'),
    path('search/', search, name="search"),
    path('details/<str:imdbId>/<str:type>/', details, name="details"),
    path('details/episode_ratings/<str:imdbID>/', episode_ratings, name="episode_ratings"),
]