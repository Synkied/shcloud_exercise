"""
Reservation viewset for api
"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from reservations.models import Reservation

from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from timezone_field.rest_framework import TimeZoneSerializerField


class ReservationResultsSetPagination(PageNumberPagination):
    page_size = 100


class ReservationFilter(FilterSet):
    # set a filterset to use filters
    # you can use: http://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#using-the-filter-fields-shortcut  # noqa
    # but it won't let you use "exclude"
    insensitive_name = filters.CharFilter(
        field_name="name",
        lookup_expr='icontains'
    )

    class Meta:
        model = Reservation
        fields = '__all__'


class ReservationSerializer(ModelSerializer):

    start_date = TimeZoneSerializerField()
    end_date = TimeZoneSerializerField()

    class Meta:
        model = Reservation
        fields = (
            'pk', 'title', 'creator_id', 'creator_name',
            'start_date', 'end_date', 'resource'
        )


class ReservationViewSet(ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = ReservationFilter
    ordering_fields = ('creation_date', )
    search_fields = (
        'pk', 'title', 'start_date', 'end_date', 'creator_id', 'creator_name'
    )
    pagination_class = ReservationResultsSetPagination

    @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        """
        Returns a list of user's reservations.
        """
        user = self.request.user
        if not user.is_admin:
            queryset = Reservation.objects.filter(creator_id=user.pk)
            serializer = ReservationSerializer(queryset, many=True)
            return Response({'results': serializer.data})

        return super(ReservationViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given reservation.
        """
        return super(ReservationViewSet, self).retrieve(*args, **kwargs)
