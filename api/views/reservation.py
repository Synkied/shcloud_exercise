"""
Reservation viewset for api
"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from reservations.models import Reservation

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class ReservationResultsSetPagination(PageNumberPagination):
    page_size = 100


class ReservationSerializer(ModelSerializer):

    class Meta:
        model = Reservation
        fields = (
            'title', 'creator_id', 'creator_name',
            'start_date', 'end_date', 'resource'
        )


class ReservationViewSet(ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    ordering_fields = ('creation_date', )
    search_fields = (
        'title', 'start_date', 'end_date', 'creator_id', 'creator_name'
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
            serializer = ReservationSerializer(queryset, many=True)
            print(serializer.data)
            return Response({'results': serializer.data})

        return super(ReservationViewSet, self).list(*args, **kwargs)

    def retrieve(self, *args, **kwargs):
        """
        Returns the given reservation.
        """
        return super(ReservationViewSet, self).retrieve(*args, **kwargs)
