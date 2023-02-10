import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.funcional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_con_login_successefully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn(
            f'Your are logged in with {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        # self.sleep(10)
