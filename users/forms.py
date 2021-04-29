from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from plan_heure.constants import GENDERS

from timezone_field import TimeZoneFormField

from users.models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        """
        Add default css-class to display bootstrap style form.
        """
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    gender = forms.ChoiceField(
        choices=GENDERS,
        required=False,
        help_text=_('Optional.')
    )
    email = forms.EmailField(
        max_length=254,
        help_text=_('Required. Enter a valid email address.')
    )
    timezone = TimeZoneFormField()

    class Meta:
        model = User
        fields = (
            'name', 'gender', 'email',
            'password1', 'password2', 'timezone',
        )
