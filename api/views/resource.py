"""
Resource viewset for api
"""
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from resources.models import Resource

from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class ResourceResultsSetPagination(PageNumberPagination):
    page_size = 100


class ResourceFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    insensitive_name = filters.CharFilter(
        field_name="name",
        lookup_expr='icontains'
    )

    class Meta:
        model = Resource
        fields = '__all__'


class ResourceSerializer(ModelSerializer):

    class Meta:
        model = Resource
        fields = (
            'pk', 'label', 'resource_type',
            'localization', 'capacity'
        )


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ResourceFilter
    ordering_fields = ('creation_date', )
    search_fields = (
        'title', 'start_date', 'end_date',
        'resource_type', 'localization',
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
