from django.contrib import admin

from resources.models import Location
from resources.models import Resource
from resources.models import ResourceType


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    empty_value_display = '-'


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    empty_value_display = '-'


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    fieldsets = (
        (None, {
            'fields': ('label',)
        }),
    )

    list_display = ('label',)
