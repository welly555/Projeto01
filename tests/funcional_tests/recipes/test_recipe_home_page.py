from unittest.mock import Patch

import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFuncionalTest


@pytest.mark.funcional_test
class RecipeHomePageTest(RecipeBaseFuncionalTest):

    @patch
    def test_recipe_home_page_without_recipes_mensages_error(self):
        self.make_recipe_bath(8)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here😥😣', body.text)
