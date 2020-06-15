from django.utils.timezone import datetime, now, make_aware
from rest_framework.serializers import ModelSerializer, ValidationError

from rains.models import Rain


class RainSerializer(ModelSerializer):
    class Meta:
        model = Rain
        fields = "__all__"

    def to_internal_value(self, data):
        date_time_str = data.get("date_time")
        try:
            date_time = datetime.strptime(date_time_str, "%Y-%m-%d, %H:%Mhs")
        except (TypeError, ValueError):
            return super().to_internal_value(data)
        data.update({"date_time": date_time})
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
    def validate_date_time(date_time):
        """
        It checks if rain_datetime is not in the future.
        """

        if now() < date_time:
            raise ValidationError("date_time must be a past datetime.")
        return date_time
