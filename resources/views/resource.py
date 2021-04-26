from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView

from resources.models import Resource
# Create your views here.


class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    context_object_name = 'resources'
    ordering = ['-creation_date']
    paginate_by = 100


class ResourceDetailView(DetailView):
    model = Resource
    context_object_name = 'resource'
