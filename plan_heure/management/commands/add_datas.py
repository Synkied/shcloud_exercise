from datetime import datetime
from datetime import timedelta
from datetime import timezone
from random import randrange
from random import uniform

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

import requests

from reservations.models import Reservation

from resources.models import Location
from resources.models import Resource
from resources.models import ResourceType

from users.models import User


class Command(BaseCommand):
    help = 'Import some test datas.'

    def add_arguments(self, parser):
        parser.add_argument('import_type', type=str, nargs='?', default='all')

    def handle(self, *args, **options):
        import_type = options.get('import_type', None)

        if import_type:
            self.stdout.write(self.style.WARNING('Starting import'))
        else:
            self.stdout.write(
                self.style.ERROR('Importing failed. Check arguments.'))
            return False

        if import_type == 'all':
            self.clear_reservations()
            self.clear_resources()
            self.clear_users()
            self.import_users()
            self.import_resources()
            self.import_reservations()
        elif import_type == 'reservations':
            self.import_reservations()
        elif import_type == 'resources':
            self.import_resources()
        elif import_type == 'clear':
            self.clear_reservations()
            self.clear_resources()
        else:
            self.stdout.write(
                self.style.ERROR('Import argument not recognized! :('))

    def clear_users(self):
        self.stdout.write(self.style.WARNING('Deleting all users...'))
        User.objects.exclude(email='synkx@hotmail.fr').delete()
        self.stdout.write(self.style.SUCCESS('All users deleted!'))

    def clear_reservations(self):
        self.stdout.write(self.style.WARNING('Deleting all reservations...'))
        Reservation.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All reservations deleted!'))

    def clear_resources(self):
        self.stdout.write(self.style.WARNING('Deleting all resources...'))
        Resource.objects.all().delete()
        ResourceType.objects.all().delete()
        Location.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All resources deleted!'))

    def import_users(self):
        self.stdout.write(self.style.WARNING('Creating some users...'))
        for i in range(randrange(10, 20)):
            label = self.random_label_generator(
                2,
                titleize=True,
                hyphens=False
            )
            email = self.random_email_generator()

            creator = User.objects.create(
                email=email,
                name=label,
            )
            creator.save()

        self.stdout.write(self.style.SUCCESS('%s users created!') % str(i + 1))

    def import_resources(self):
        # Create Locations
        self.stdout.write(self.style.WARNING('Creating some locations...'))
        for i in range(randrange(5, 10)):
            label = self.random_label_generator(1)

            latitude = uniform(-90, 90)
            longitude = uniform(-180, 180)

            floor = randrange(60)

            location = Location()
            location.label = label
            location.latitude = latitude
            location.longitude = longitude
            location.floor = floor

            location.save()

        self.stdout.write(
            self.style.SUCCESS('%s locations created!' % str(i + 1))
        )

        # Create Resource Types
        self.stdout.write(
            self.style.WARNING('Creating some resource types...')
        )
        for i in range(randrange(5, 20)):
            label = self.random_label_generator(1, capitalize=True)

            resource_type = ResourceType()
            resource_type.label = label
            resource_type.save()

        self.stdout.write(
            self.style.SUCCESS('%s resource types created!' % str(i + 1))
        )

        # Create Resources
        self.stdout.write(self.style.WARNING('Creating some resources...'))
        for i in range(randrange(5, 10)):
            label = self.random_label_generator(1, titleize=True)
            capacity = randrange(1000)

            resource_type = ResourceType.objects.order_by('?')[0]
            location = Location.objects.order_by('?')[0]

            resource = Resource()
            resource.resource_type = resource_type
            resource.label = label
            resource.location = location
            resource.capacity = capacity
            resource.save()

        self.stdout.write(self.style.SUCCESS('%s resources created!' % i))

    def import_reservations(self):
        self.stdout.write(self.style.WARNING('Creating some reservations...'))

        reservations_created = 0

        for i in range(randrange(30, 60)):
            label = self.random_label_generator(1, titleize=True)
            resource = Resource.objects.order_by('?')[0]
            creator = User.objects.order_by('?')[0]

            beginning_date = datetime.now(timezone.utc)
            ending_date = beginning_date + timedelta(days=7)

            start_date = self.random_date(beginning_date, ending_date)
            corresponding_ending_date = start_date + timedelta(
                hours=randrange(1, 5)
            )

            reservation = Reservation()
            reservation.title = label
            reservation.start_date = start_date
            reservation.end_date = corresponding_ending_date
            reservation.resource = resource
            reservation.creator = creator

            try:
                reservation.save()
            except ValidationError:
                continue

            reservations_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                '%s reservations created!' % reservations_created
            )
        )

    def random_label_generator(self, length=3, word_length=2,
                               titleize=False, capitalize=False, hyphens=True):
        word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

        response = requests.get(word_site)
        WORDS = response.content.splitlines()

        label = ''
        for i in range(length):
            idx = 0
            while not len(WORDS[idx]) > word_length:
                idx = randrange(len(WORDS))
            if i == 0:
                label += '%s' % WORDS[idx].decode('ascii')
            else:
                if hyphens:
                    label += '-%s' % WORDS[idx].decode('ascii')
                else:
                    label += ' %s' % WORDS[idx].decode('ascii')

        if titleize:
            label = label.title()
        if capitalize:
            label = label.upper()
        return label

    def random_email_generator(self):
        label = self.random_label_generator(3)
        email = label.replace('-', '@', 1)
        email = email.replace('-', '.', 1)
        return email

    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)
