from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFuncionalTest


@pytest.mark.funcional_test
class RecipeHomePageTest(RecipeBaseFuncionalTest):

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_mensages_error(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here😥😣', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_seach_imput_can_find_correct(self):
        recipes = self.make_recipe_bath()
        tittle_needed = 'this is what I need'
        recipes[0].tittle = tittle_needed
        recipes[0].save()
        self.browser.get(self.live_server_url)
        seach_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        seach_input.send_keys(tittle_needed)
        seach_input.send_keys(Keys.ENTER)

        self.assertIn(
            tittle_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-contente-list').text
        )
        self.sleep(6)

    @patch('recipes.views.PER_PAGE', new=4)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_bath()

        self.browser.get(self.live_server_url)

        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            4
        )
        self.sleep(10)
