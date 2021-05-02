from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from users.forms import SignUpForm


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Simple sign up view.
    """
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = _("Your profile was created successfully")
