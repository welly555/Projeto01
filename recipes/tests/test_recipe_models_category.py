from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCaregoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(name='testing category')
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_max_length_65_chars(self):
        self.category.name = 'A' * 65
        with self.assertRaises(ValidationError):
            self.category.full_clean()
