from django.urls import path

from recipes.views import Sobre, contato, home

urlpatterns = [
    path('', home),
    path('contato/', contato),
    path('sobre/', Sobre)
]
