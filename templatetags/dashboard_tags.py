from django import template

from reservations.models import Reservation

from resources.models import Resource

register = template.Library()


@register.inclusion_tag('tags/activity.html', takes_context=True)
def latest_reservations(context):
    user = context['user']
    reservations = Reservation.objects.filter(creator_id=user.pk)

    return {
        'reservations': reservations
    }


@register.inclusion_tag('tags/activity.html', takes_context=True)
def latest_resources(context):
    resources = Resource.objects.all()

    return {
        'resources': resources
    }
