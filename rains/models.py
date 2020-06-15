from django.db.models import CASCADE, DateTimeField, FloatField, ForeignKey

from fields.models import Field
from utils.models import TimeStampModel


class Rain(TimeStampModel):
    field = ForeignKey(to=Field, on_delete=CASCADE, related_name="rains")
    milimeters = FloatField()
    date_time = DateTimeField()

    class Meta:
        db_table = "rains"

    def __str__(self):
        """
        Returns a Rain's string representation.
        """

        return (
            f"id={self.id}, land={self.field.id}, milimeters={round(self.milimeters, 3)}, "
            f"rain_datetime={self.date_time.strftime('(%Y-%m-%d, %H:%Mhs)')}"
        )
