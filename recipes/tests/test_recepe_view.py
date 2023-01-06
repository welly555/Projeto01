from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewTest(RecipeTestBase):

    def test_recipe_home_view_function_acept(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

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

    def test_recipe_home_template_not_published(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Recipe tittle', content)

    def test_recipe_category_view_function_acept(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

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

    def test_recipe_detail_view_function_acept(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_recipe_not_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 100}))
        self.assertEqual(response.status_code, 404)

    def test_detail_template_loads_recipes(self):
        tittle = 'the is a detail page test - one load recipe'
        self.make_recipe(tittle=tittle)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(tittle, content)

    def test_recipe_detail_template_loads_recipes(self):
        """Test detail is_published False """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', args=(recipe.id,)))
        self.assertEqual(response.status_code, 404)
