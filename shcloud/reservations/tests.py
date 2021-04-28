from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

import pytz

from reservations.models import Reservation

from resources.models import Localization
from resources.models import Resource
from resources.models import ResourceType

from users.models import User


class ReservationTestCase(TestCase):

    def setUp(self):
        self.creator = User.objects.create(
            email='toto@titi.fr',
            name='The Creator',
        )

        localization = Localization()
        localization.label = 'B22'
        localization.latitude = 48.856614
        localization.longitude = 2.3522219
        localization.floor = 1
        localization.save()

        resource_type = ResourceType()
        resource_type.label = 'salle de conférence'
        resource_type.save()

        self.resource_one = Resource()
        self.resource_one.resource_type = resource_type
        self.resource_one.label = 'Salle de conférence XT'
        self.resource_one.localization = localization
        self.resource_one.capacity = 100
        self.resource_one.save()

    def test_reservations_overlapping_dates(self):
        reservation_one = Reservation()
        reservation_one.title = 'A reservation'
        reservation_one.start_date = datetime(
            2021, 4, 28, 15, 15, 0, tzinfo=pytz.UTC
        )
        reservation_one.end_date = datetime(
            2021, 4, 28, 16, 15, 0, tzinfo=pytz.UTC
        )
        reservation_one.resource = self.resource_one
        reservation_one.creator = self.creator

        with self.assertNumQueries(4):
            reservation_one.save()

        reservation_two = Reservation()
        reservation_two.title = 'A reservation'
        reservation_two.start_date = datetime(
            2021, 4, 28, 16, 0, 0, tzinfo=pytz.UTC
        )
        reservation_two.end_date = datetime(
            2021, 4, 28, 17, 0, 0, tzinfo=pytz.UTC
        )
        reservation_two.resource = self.resource_one
        reservation_two.creator = self.creator

        with self.assertNumQueries(3):
            with self.assertRaises(ValidationError):
                reservation_two.save()

    def test_reservations_wrong_dates(self):
        reservation_one = Reservation()
        reservation_one.title = 'A reservation'
        reservation_one.start_date = datetime(
            2021, 4, 28, 17, 15, 0, tzinfo=pytz.UTC
        )
        reservation_one.end_date = datetime(
            2021, 4, 28, 16, 15, 0, tzinfo=pytz.UTC
        )
        reservation_one.resource = self.resource_one
        reservation_one.creator = self.creator

        with self.assertNumQueries(2):
            with self.assertRaises(ValidationError):
                reservation_one.save()
