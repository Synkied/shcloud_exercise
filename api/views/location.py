"""
Location viewset for api
"""
from resources.models import Location

from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class LocationResultsSetPagination(PageNumberPagination):
    page_size = 100


class LocationSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Location
        fields = (
            'label', 'latitude', 'longitude', 'floor'
        )


class LocationViewSet(ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    ordering_fields = ('creation_date', )
    search_fields = (
        'title', 'start_date', 'end_date',
    )
    pagination_class = LocationResultsSetPagination

    def list(self, *args, **kwargs):
        """
        Returns a list of all Locations.
        """
        return super(LocationViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given Location.
        """
        return super(LocationViewSet, self).retrieve(*args, **kwargs)
