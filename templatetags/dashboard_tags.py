from django import template

from reservations.models import Reservation

from resources.models import Resource

register = template.Library()


@register.inclusion_tag('tags/activity.html', takes_context=True)
def latest_reservations(context):
    user = context['user']
    reservations = Reservation.objects.filter(creator_id=user.pk)[:8]

    return {
        'reservations': reservations,
        'user': user,
    }


@register.inclusion_tag('tags/activity.html', takes_context=True)
def latest_resources(context):
    user = context['user']
    resources = Resource.objects.all()[:8]

    return {
        'resources': resources,
        'user': user,
    }
