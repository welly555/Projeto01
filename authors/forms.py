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
        add_placeholder(self.fields['username'], 'You username')
        add_placeholder(self.fields['email'], 'You e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: jhon')
        add_placeholder(self.fields['last_name'], 'Ex.: doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'password must not by empy'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
    )

    password_confirmed = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
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
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password'
        }
        help_texts = {
            'email': 'the e-mail must be valid'
        }
        error_messages = {
            'username': {
                'required': 'this field must not by empy'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your Firstname here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise forms.ValidationError(
                'não digite %(invalid)s nesse campo',
                code='invalid',
                params={'invalid': 'atenção'},
            )
        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'atenção' in data:
            raise ValidationError(
                'não digite %(invalid)s nesse campo',
                code='invalid',
                params={'invalid': 'atenção'},
            )
        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')

        if password != password_confirmed:
            raise ValidationError({
                'password_confirmed': 'password different'
            })
