from django.contrib import admin

from reservations.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    empty_value_display = '-'

    list_display = (
        'title', 'resource', 'start_date', 'end_date', 'creator',
        'creation_date'
    )
