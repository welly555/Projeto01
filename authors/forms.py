import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(passvord):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(passvord):
        raise ValidationError(
            ('the pass word must have at last\n '
             'one letter;\n '
             'one uppercase letter;\n '
             'a number;\n '
             'and at last 8 characters\n '
             ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: jhon')
        add_placeholder(self.fields['last_name'], 'Ex.: doe')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(
            self.fields['password_confirmed'], 'Repeat your password')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is requirid'},
        required=True,
        label='E-mail',
        help_text='the e-mail must be valid'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password'
    )

    password_confirmed = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Password Confirmed',
        error_messages={
            'required': 'Please, repeat your password'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        labels = {
            'username': 'Username',
        }
        error_messages = {
            'username': {
                'required': 'this field must not by empy'
            }
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')

        if password != password_confirmed:
            raise ValidationError({
                'password_confirmed': 'password different'
            })
