"""
Urls for api
"""
from api.views import location
from api.views import reservation
from api.views import resource
from api.views import resourcetype

from rest_framework import routers

router = routers.DefaultRouter()

router.register(
    r'location',
    location.LocationViewSet,
    basename='location',
)
router.register(
    r'reservation',
    reservation.ReservationViewSet,
    basename='reservation',
)
router.register(
    r'resource',
    resource.ResourceViewSet,
    basename='resource',
)
router.register(
    r'resourcetype',
    resourcetype.ResourceTypeViewSet,
    basename='resourcetype',
)

urlpatterns = router.urls
