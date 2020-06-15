from django.contrib.admin import ModelAdmin, site

from rains.models import Rain


class RainAdmin(ModelAdmin):
    model_fields_tuple = ("id", "field", "milimeters", "rain_datetime")

    # set presentational fields
    list_display = model_fields_tuple
    search_fields = model_fields_tuple
    ordering = ("id",)

    # set detail fields
    fields = ["field", "milimeters", "rain_datetime"]


site.register(Rain, RainAdmin)
