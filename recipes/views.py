from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from utils.pagination import make_pagination_range

# from utils.recipes.factory import make_recipe

# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    paginator = Paginator(recipes, 6)
    page_obj = paginator.get_page(current_page)

    paginator_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )
    context = {
        'recipes': page_obj,
        'paginator_range': paginator_range}
    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, is_published=True).order_by('-id'))

    context = {'recipes': recipes,
               'tittle': f'{recipes[0].category.name}  - Category |'}
    return render(request, 'recipes/pages/category.html', context=context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    context = {'recipe': recipe, 'is_detail_page': True, }
    return render(request, 'recipes/pages/recipe-view.html', context=context)


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipe = Recipe.objects.filter(
        Q(
            Q(tittle__icontains=search_term) | Q(
                description__icontains=search_term),
        ),
        is_published=True

    )
    recipe = recipe.filter(is_published=True)

    return render(request, 'recipes/pages/search.html', {
        'page_tittle': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipe
    })
