from django.db import models
from django.utils.translation import gettext_lazy as _


class ResourceType(models.Model):
    """
    A ResourceType model.
    """
    label = models.CharField(
        max_length=64,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return 'ResourceType %s' % self.label

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
        max_length=64,
    )

    latitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
    )
    longitude = models.DecimalField(
        max_digits=22,
        decimal_places=16,
    )
    floor = models.SmallIntegerField()

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return 'Localization %s' % self.label

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
        related_name='resource_type',
        verbose_name=_('resource type')
    )

    label = models.CharField(
        max_length=64,
    )

    localization = models.ForeignKey(
        Localization,
        on_delete=models.PROTECT,
        related_name='localization',
    )

    capacity = models.PositiveSmallIntegerField()

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return 'Resource %s' % self.label

    class Meta:
        ordering = ['-creation_date']
        verbose_name = _('resource')
        verbose_name_plural = _('resources')
        db_table = 'core_resource'
