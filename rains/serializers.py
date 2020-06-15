from django.utils.timezone import datetime, now, make_aware
from rest_framework.serializers import ModelSerializer, ValidationError

from rains.models import Rain


class RainSerializer(ModelSerializer):
    class Meta:
        model = Rain
        fields = "__all__"

    def to_internal_value(self, data):
        rain_date_time_str = data.get("rain_datetime")
        try:
            rain_datetime = datetime.strptime(rain_date_time_str, "%Y-%m-%d, %H:%Mhs")
        except (TypeError, ValueError):
            return super().to_internal_value(data)
        data.update({"rain_datetime": rain_datetime})
        return super().to_internal_value(data)

    @staticmethod
    def validate_milimeters(milimeters):
        """
        It checks if milimeters is greater than 0.
        """

        if milimeters < 0:
            raise ValidationError("milimeters must be 0 or positive value.")
        return milimeters

    @staticmethod
    def validate_rain_datetime(rain_datetime):
        """
        It checks if rain_datetime is not in the future.
        """

        if now() < rain_datetime:
            raise ValidationError("rain_datetime must be a past datetime.")
        return rain_datetime
