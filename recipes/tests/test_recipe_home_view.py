from unittest.mock import patch

import pytest
from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


@pytest.mark.slow
class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_home_view_function_acept(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_recipe_home_view_return_status_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_template_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def teste_recipe_template_home_show_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf8'))

    def test_recipe_home_template_loads_recipes(self):
        """Test recipe is_published False """
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf8'))

    def test_recipe_home_is_paginatior(self):

        self.make_recipe_bath(18)

        with patch('recipes.views.PER_PAGE', new=5):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 6)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_bath(qty=8)

        with patch('recipes.views.PER_PAGE', new=5):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(response.context['recipes'].number, 2)
