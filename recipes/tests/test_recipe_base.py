from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='132456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            tittle='Recipe tittle',
            description='Recipe descripton',
            slug='recipe_slug',
            preparation_time=10,
            preparation_time_unit='minuyos',
            servings=5,
            servings_unit='porções',
            preparation_steps='recipe preparetion steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        return super().setUp()
