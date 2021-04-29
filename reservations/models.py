from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from resources.models import Resource


class Reservation(models.Model):
    """
    A Reservation model.
    """
    title = models.CharField(
        max_length=256,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    resource = models.ForeignKey(
        Resource,
        on_delete=models.PROTECT,
        related_name='reservation',
        verbose_name=_('reservation')
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_('creator')
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        auto_now=True,
    )

    def check_overlapping_dates(self):
        reservations = Reservation.objects.filter(
            ~Q(pk=self.pk),
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
            resource=self.resource,
        )

        if len(reservations):
            raise ValidationError(
                _('Overlapping dates, another reservation is already registered for this resource.')  # noqa
            )

    def check_wrong_dates(self):

        if self.start_date > self.end_date:
            raise ValidationError(
                _('Incorrect dates.')  # noqa
            )

    def clean(self):
        self.check_wrong_dates()
        self.check_overlapping_dates()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('reservation_detail', args=[self.pk])

    @property
    def creator_name(self):
        return self.creator.name

    def __str__(self):
        return 'Reservation %s' % self.title

    class Meta:
        ordering = ['-update_date']
        verbose_name = _('reservation')
        verbose_name_plural = _('reservations')
        db_table = 'core_reservation'
        indexes = [
            models.Index(fields=['title'], name='title_idx')
        ]
