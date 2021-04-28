"""
Reservation viewset for api
"""
import json

from django.http import JsonResponse

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from reservations.models import Reservation

from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


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

    # @method_decorator(cache_page(60*2))
    def list(self, *args, **kwargs):
        """
        Returns a list of user's reservations.
        """
        user = self.request.user
        if not user.is_admin:
            queryset = Reservation.objects.filter(creator_id=user.pk)
            # other_reservations = Reservation.objects.exclude(
            #     creator_id=user.pk
            # ).values('pk')

            # queryset = queryset | other_reservations
            serializer = ReservationSerializer(queryset, many=True)
            # jsonified_data = {}

            # list_other_reservations = list(other_reservations)
            # other_reservations_pks = [
            #     i for d in list_other_reservations for i in d.values()
            # ]

            # remove other reservations infos
            # for d in serializer.data:
            #     jsonified_data[d['pk']] = d
            #     if d['pk'] in other_reservations_pks:
            #         d['title'] = 'Private reservation n° %s' % d['pk']
            #         d['creator_name'] = ''
            #         d['creator_id'] = ''

            # return JsonResponse(
            #     {'results': serializer.data},
            #     status=200,
            #     safe=False
            # )
            return Response({'results': serializer.data})

        return super(ReservationViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given reservation.
        """
        return super(ReservationViewSet, self).retrieve(*args, **kwargs)
