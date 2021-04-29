from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import SignUpForm


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your profile was created successfully"
