from django.db import models
from django.utils.translation import gettext_lazy as _


class ResourceType(models.Model):
    """
    A ResourceType model.
    """
    label = models.CharField(
        _('label'),
        max_length=64,
    )

    creation_date = models.DateTimeField(
        _('creation date'),
        auto_now_add=True,
    )

    def __str__(self):
        return '%s' % self.label

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('resource type')
        verbose_name_plural = _('resource types')
        db_table = 'core_resourcetype'


class Localization(models.Model):
    """
    A Localization model.
    """
    label = models.CharField(
        _('label'),
        max_length=64,
    )

    latitude = models.DecimalField(
        _('latitude'),
        max_digits=22,
        decimal_places=16,
    )
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=22,
        decimal_places=16,
    )
    floor = models.SmallIntegerField(
        _('floor')
    )

    creation_date = models.DateTimeField(
        _('creation date'),
        auto_now_add=True,
    )

    def __str__(self):
        return '%s' % self.label

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('localization')
        verbose_name_plural = _('localizations')
        db_table = 'core_localization'


class Resource(models.Model):
    """
    A Resource model.
    """
    resource_type = models.ForeignKey(
        ResourceType,
        on_delete=models.PROTECT,
        related_name='resource',
        verbose_name=_('resource type')
    )

    label = models.CharField(
        _('label'),
        max_length=64,
    )

    localization = models.ForeignKey(
        Localization,
        on_delete=models.PROTECT,
        related_name='resource',
        verbose_name=_('localization')
    )

    capacity = models.PositiveSmallIntegerField(
        _('capacity')
    )

    creation_date = models.DateTimeField(
        _('creation date'),
        auto_now_add=True,
    )

    @property
    def all_reservations(self):
        return self.reservations.all()

    @property
    def long_name(self):
        return '%s (%s - %s p.)' % (
            self.label,
            self.localization.label,
            self.capacity
        )

    def __str__(self):
        return '%s (%s - %s p.)' % (
            self.label,
            self.localization.label,
            self.capacity
        )

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('resource')
        verbose_name_plural = _('resources')
        db_table = 'core_resource'
