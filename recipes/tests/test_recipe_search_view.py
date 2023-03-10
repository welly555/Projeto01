from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_seach_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func.view_class, views.RecipeListViewSeach)

    def test_recipe_search_loads_ok_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipes_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_tittle_and_escaped(self):
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;teste&quot; | Recipes',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_tittle(self):
        tittle1 = 'This is recipe one'
        tittle2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            tittle=tittle1,
            author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two',
            tittle=tittle2,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={tittle1}')
        response2 = self.client.get(f'{search_url}?q={tittle2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
