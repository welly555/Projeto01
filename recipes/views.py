
from django.shortcuts import render

from utils.recipes.factory import make_recipe

# Create your views here.


def home(request):

    context = {'recipes': [make_recipe() for _ in range(10)]}
    return render(request, 'recipes/pages/home.html', context=context)


def recipes(request, id):
    context = {'recipes': [make_recipe()]}
    return render(request, 'recipes/pages/recipe-view.html', context=context)
