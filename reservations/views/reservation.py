from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from reservations.forms import ReservationCreationForm
from reservations.models import Reservation
# Create your views here.


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    context_object_name = 'reservations'
    ordering = ['-creation_date']
    paginate_by = 20

    def get_context_data(self, **kwargs):

        context = super(ReservationListView, self).get_context_data(**kwargs)

        return context

    def get_queryset(self):
        """
        Only show current user reservations if not admin
        """
        qs = super(ReservationListView, self).get_queryset()
        if not self.request.user.is_admin:
            qs = Reservation.objects.filter(creator=self.request.user)

        return qs


class ReservationDetailView(DetailView):
    model = Reservation
    context_object_name = 'reservation'


class ReservationCreationView(CreateView):
    model = Reservation
    template_name = 'reservations/reservation_create.html'
    form_class = ReservationCreationForm
    success_url = '/reservation/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return super(ReservationCreationView, self).form_valid(form)


class ReservationEditView(UpdateView):
    model = Reservation
    template_name = 'reservations/reservation_create.html'
    form_class = ReservationCreationForm
    success_url = '/reservation/'


class ReservationCancelView(DeleteView):
    model = Reservation
    success_url = '/reservation/'
