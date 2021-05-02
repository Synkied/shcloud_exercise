from django import forms
from django.utils.translation import gettext_lazy as _

from reservations.models import Reservation

from resources.models import Location
from resources.models import ResourceType


class ReservationCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Add default CSS-class to display Bootstrap style form.
        """
        super(ReservationCreationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    # custom fields
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
    )
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        required=False,
    )

    class Meta:
        model = Reservation
        fields = [
            'title',
            'location',
            'resource_type',
            'resource',
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': forms.DateTimeInput(
                format=('%m/%d/%Y %H:%M'),
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Select a date and time'),
                    'type': 'datetime-local'
                }
            ),
            'end_date': forms.DateTimeInput(
                format=('%m/%d/%Y %H:%M'),
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Select a date and time'),
                    'type': 'datetime-local'
                }
            ),
        }
