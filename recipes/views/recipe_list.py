import os

from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    paginate_by = None
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, paginator_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {'recipes': page_obj, 'paginator_range': paginator_range}
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):

    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = get_list_or_404(qs.filter(
            is_published=True,
            category__id=self.kwargs.get('category_id'),
        ))

        self.name = qs[0].category.name

        return qs

    def get_context_data(self, *args, **kwargs):

        ctx = super().get_context_data(*args, **kwargs)
        page_obj, paginator_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        ctx.update(
            {'recipes': page_obj, 'paginator_range': paginator_range,
             'tittle': f'{self.name}'}
        )
        return ctx


class RecipeListViewSeach(RecipeListViewBase):
    ...
