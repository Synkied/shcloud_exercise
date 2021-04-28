"""
Localization viewset for api
"""
from resources.models import Localization

from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class LocalizationResultsSetPagination(PageNumberPagination):
    page_size = 100


class LocalizationSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Localization
        fields = (
            'label', 'latitude', 'longitude', 'floor'
        )


class LocalizationViewSet(ReadOnlyModelViewSet):
    queryset = Localization.objects.all()
    serializer_class = LocalizationSerializer
    ordering_fields = ('creation_date', )
    search_fields = (
        'title', 'start_date', 'end_date',
    )
    pagination_class = LocalizationResultsSetPagination

    def list(self, *args, **kwargs):
        """
        Returns a list of all localizations.
        """
        return super(LocalizationViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given localization.
        """
        return super(LocalizationViewSet, self).retrieve(*args, **kwargs)
