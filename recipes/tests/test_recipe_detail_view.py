from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_acept(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_return_404_if_recipe_not_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)

    def test_detail_template_loads_recipes(self):
        tittle = 'the is a detail page test - one load recipe'
        self.make_recipe(tittle=tittle)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(tittle, content)

    def test_recipe_detail_template_loads_recipes(self):
        """Test detail is_published False """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)
