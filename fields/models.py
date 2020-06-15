from django.conf import settings

from utils.models import TimeStampModel
from django.db.models import CASCADE, CharField, DecimalField, FloatField, ForeignKey


class Field(TimeStampModel):
    owner = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="fields")
    name = CharField(max_length=20)
    hectares = FloatField()
    latitude = DecimalField(max_digits=8, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = "fields"

    def __str__(self):
        """
        Returns a Field's string representation.
        """

        return (
            f"id={self.id}, name={self.name}, owner={self.owner.id}, hectares={round(self.hectares, 3)}, "
            f"latitude={round(self.latitude, 2)}, longitude={round(self.longitude, 2)}"
        )
