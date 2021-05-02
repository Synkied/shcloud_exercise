from django.test import TestCase

from resources.models import Location
from resources.models import Resource
from resources.models import ResourceType


class ResourceTestCase(TestCase):

    def setUp(self):
        self.location_b22 = Location()
        self.location_b22.label = 'B22'
        self.location_b22.latitude = 48.856614
        self.location_b22.longitude = 2.3522219
        self.location_b22.floor = 1
        self.location_b22.save()

        self.resource_type_conference_room = ResourceType()
        self.resource_type_conference_room.label = 'salle de conférence'
        self.resource_type_conference_room.save()

    def test_save_new_resource(self):

        resource_one = Resource()
        resource_one.resource_type = self.resource_type_conference_room
        resource_one.label = 'Salle de conférence XT'
        resource_one.location = self.location_b22
        resource_one.capacity = 100
        resource_one.save()

        with self.assertNumQueries(1):
            resource_one.save()
