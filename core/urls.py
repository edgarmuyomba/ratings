from django.urls import path 
from django.views.generic import TemplateView
from .views import search, details

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name="core/index.html"), name='index'),
    path('search/', search, name="search"),
    path('details/<str:imdbId>/<str:type>/', details, name="details"),
]