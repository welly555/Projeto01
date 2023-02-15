from collections import defaultdict

from django import forms
from django.forms import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'tittle',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleand_data = self.cleaned_data
        tittle = cleand_data.get('tittle')
        description = cleand_data.get('description')
        preparation_steps = cleand_data.get('preparation_steps')

        if len(tittle) < 5:
            self._my_errors['tittle'].append(
                'tittle must have at least 5 chars.')
        if len(description) < 5:
            self._my_errors['description'].append(
                'description must have at least 5 chars.')
        if len(preparation_steps) < 15:
            self._my_errors['preparation_steps'].append(
                'preparation_steps must have at least 15 chars.')

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_errors['preparation_time'].append(
                'Not allowed number negative')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value):
            self._my_errors['servings'].append(
                'Not allowed number negative')

        return field_value
