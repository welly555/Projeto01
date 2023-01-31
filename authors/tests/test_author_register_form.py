# from django.test import TestCase
from unittest import TestCase

from django.test import TestCase as djangoTesteCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: jhon'),
        ('last_name', 'Ex.: doe'),
        ('password', 'Your password'),
        ('password_confirmed', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('email', 'the e-mail must be valid'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
        ('username', 'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.')  # noqa: E501
    ])
    def test_fields_help_test(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password_confirmed', 'Password Confirmed')
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_placeholder = form[field].field.label
        self.assertEqual(current_placeholder, label)


class AuthorRegisterFormIntegrationTest(djangoTesteCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'username',
            'first_name': 'First',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirmed': 'Str0ngP@ssword1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'this field must not by empy'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password_confirmed', 'Please, repeat your password'),
        ('email', 'E-mail is requirid')
    ])
    def test_field_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
