import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from recipes.tests.test_recipe_base import RecipeMixin
from utils.browser import make_chrome_browser


class RecipeBaseFuncionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self, *args, **kwargs):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self, *args, **kwargs):
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)