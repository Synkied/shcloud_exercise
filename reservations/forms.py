from django import forms

from reservations.models import Reservation

from resources.models import Localization
from resources.models import ResourceType


class ReservationCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Add default css-class to display bootstrap style form.
        """
        super(ReservationCreationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    # custom fields
    localization = forms.ModelChoiceField(
        queryset=Localization.objects.all(),
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
            'resource_type',
            'localization',
            'resource',
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': forms.DateTimeInput(
                format=('%m/%d/%Y %H:%M'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date and time',
                    'type': 'datetime-local'
                }
            ),
            'end_date': forms.DateTimeInput(
                format=('%m/%d/%Y %H:%M'),
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date and time',
                    'type': 'datetime-local'
                }
            ),
        }
