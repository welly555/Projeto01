from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_acept(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_return_404_if_recipe_not_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_category_template_loads_recipes(self):
        tittle = 'the is a category test'
        self.make_recipe(tittle=tittle)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn(tittle, content)

    def test_recipe_category_template_loads_recipes(self):
        """Test category is_published False """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', args=(recipe.category.id,)))
        self.assertEqual(response.status_code, 404)
