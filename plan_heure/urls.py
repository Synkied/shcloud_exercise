"""plan_heure URL Configuration
"""
import debug_toolbar

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout_then_login
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView


class WelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'welcome.html'


urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('', WelcomeView.as_view()),
    path('', include('reservations.urls')),
    path('', include('resources.urls')),
    path('api/', include('api.urls')),
    path('login/', LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
