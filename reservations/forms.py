from django import forms

from reservations.models import Reservation


class ReservationCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationCreationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Reservation
        fields = [
            'title',
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
