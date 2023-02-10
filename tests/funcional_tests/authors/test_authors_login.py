import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.funcional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def create_form(self, username, password):
        user = User.objects.create_user(
            username=username, password=password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(password)

        form.submit()

    def test_user_valid_data_con_login_successefully(self):
        self.create_form('my_user', 'pass')

        self.assertIn(
            'Your are logged in with my_user.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raise_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        self.sleep(5)

    def test_user_invalid_username_or_password(self):
        self.create_form(' ', ' ')

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_credentials_invalid(self):
        string_password = 'pass'
        user = User.objects.create_user(  # noqa: E841
            username='My_user', password=string_password)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys('my_user1')
        password_field.send_keys('aknsdka')

        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
