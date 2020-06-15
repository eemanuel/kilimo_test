from django.contrib.admin import ModelAdmin, site, TabularInline

from fields.models import Field
from rains.models import Rain


class RainInline(TabularInline):
    model = Rain
    fields = ("id",)


class FieldAdmin(ModelAdmin):

    # set presentational fields
    list_display = ("id", "owner", "name", "hectares")
    search_fields = ("id", "name",)
    ordering = ("id",)

    # set detail fields
    inlines = [RainInline]  # only with a model in foreignkey
    fields = [
        "owner",
        "name",
        "hectares",
        "latitude",
        "longitude",
    ]


site.register(Field, FieldAdmin)
