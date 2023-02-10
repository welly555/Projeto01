from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_logout_using_get_method(self):
        password_string = 'my_pass'
        user = User.objects.create_user(
            username='my_user', password=password_string,)
        self.client.login(username=user.username, password=password_string)

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_tries_logout_anouther_user(self):
        password_string = 'my_pass'
        user = User.objects.create_user(
            username='my_user', password=password_string,)
        self.client.login(username=user.username, password=password_string)

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user',
                'password': 'another_pass'
            },
            follow=True)

        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        password_string = 'my_pass'
        user = User.objects.create_user(
            username='my_user', password=password_string,)
        self.client.login(username=user.username, password=password_string)

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user',
            },
            follow=True)

        self.assertIn(
            'logout success',
            response.content.decode('utf-8')
        )
