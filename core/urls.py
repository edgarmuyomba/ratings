from django.urls import path 
from django.views.generic import TemplateView
from .views import search, details, episode_ratings
from django.conf.urls.static import static
from ratings.settings import STATIC_URL, STATIC_ROOT

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name="core/index.html"), name='index'),
    path('search/', search, name="search"),
    path('details/episode_ratings/<str:imdbID>/', episode_ratings, name="episode_ratings"),
    path('details/<str:imdbId>/<str:type>/', details, name="details"),
] + static(STATIC_URL, document_root=STATIC_ROOT)