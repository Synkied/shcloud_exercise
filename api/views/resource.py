"""
Resource viewset for api
"""
from resources.models import Resource

from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class ResourceResultsSetPagination(PageNumberPagination):
    page_size = 100


class ResourceSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Resource
        fields = (
            'label', 'resource_type',
            'localization', 'capacity'
        )


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    ordering_fields = ('creation_date', )
    search_fields = (
        'title', 'start_date', 'end_date',
    )
    pagination_class = ResourceResultsSetPagination

    def list(self, *args, **kwargs):
        """
        Returns a list of all resources.
        """
        return super(ResourceViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given resource.
        """
        return super(ResourceViewSet, self).retrieve(*args, **kwargs)
