"""
ResourceType viewset for api
"""
from resources.models import ResourceType

from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class ResourceTypeResultsSetPagination(PageNumberPagination):
    page_size = 100


class ResourceTypeSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ResourceType
        fields = (
            'label',
        )


class ResourceTypeViewSet(ReadOnlyModelViewSet):
    queryset = ResourceType.objects.all()
    serializer_class = ResourceTypeSerializer
    ordering_fields = ('creation_date', )
    search_fields = (
        'label',
    )
    pagination_class = ResourceTypeResultsSetPagination

    def list(self, *args, **kwargs):
        """
        Returns a list of all resourcetypes.
        """
        return super(ResourceTypeViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given resourcetype.
        """
        return super(ResourceTypeViewSet, self).retrieve(*args, **kwargs)
