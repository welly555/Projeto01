
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from utils.pagination import make_pagination

# from utils.recipes.factory import make_recipe

# Create your views here.

PER_PAGES = 9


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, paginator_range = make_pagination(request, recipes, PER_PAGES)

    context = {
        'recipes': page_obj,
        'paginator_range': paginator_range}
    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, is_published=True).order_by('-id'))

    page_obj, paginator_range = make_pagination(request, recipes, PER_PAGES)

    context = {'recipes': page_obj,
               'paginator_range': paginator_range,
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

    recipes = Recipe.objects.filter(
        Q(
            Q(tittle__icontains=search_term) | Q(
                description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    page_obj, paginator_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/search.html', {
        'page_tittle': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'paginator_range': paginator_range,
        'additional_url_query': f'&q={search_term}',
    })
