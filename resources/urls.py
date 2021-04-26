"""
Reservations urls
"""
from django.urls import path

from resources.views import resource

urlpatterns = [
    path('resource/',
         resource.ResourceListView.as_view(),
         name='resource_list'),
    path('resource/<int:pk>/',
         resource.ResourceDetailView.as_view(),
         name='resource_detail'),
]
