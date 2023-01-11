from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='teste default'),
            author=self.make_author(username='newuser'),
            tittle='Recipe tittle',
            description='Recipe descripton',
            slug='recipe-slug-for-no-default',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='recipe preparetion steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('tittle', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparations_steps_is_html_is_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparations_steps_is_html is not false')

    def test_recipe_is_published_is_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not false')

    def test_recipe_string_representation(self):
        needed = 'Teste representation'
        self.recipe.tittle = 'Teste representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            'Teste representation',
            msg=f'Recipe string representation must be "{needed}"'
        )
