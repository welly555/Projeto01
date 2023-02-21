import os

from django.shortcuts import get_object_or_404, render

from recipes.models import Recipe

# from utils.recipes.factory import make_recipe

# Create your views here.

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    context = {'recipe': recipe, 'is_detail_page': True, }
    return render(request, 'recipes/pages/recipe-view.html', context=context)
