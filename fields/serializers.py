from fields.models import Field

from rest_framework.serializers import ModelSerializer, ValidationError


class FieldBaseSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"


class FieldSerializer(FieldBaseSerializer):
    @staticmethod
    def validate_hectares(hectares):
        """
        It checks if hectares is positive or raise ValidationError.
        """

        if hectares <= 0:
            raise ValidationError(f"hectares must be positive.")
        return hectares

    @staticmethod
    def validate_latitude(latitude):
        """
        It checks if latitude is between -90 and 90 or raise ValidationError.
        """

        if latitude < -90.0 or 90.0 < latitude:
            raise ValidationError(f"latitude must be between -90 and 90.")
        return latitude

    @staticmethod
    def validate_longitude(longitude):
        """
        It checks if latitude is between -180 and 180 or raise ValidationError.
        """

        if longitude < -180.0 or 180.0 < longitude:
            raise ValidationError(f"longitude must be between -180 and 180.")
        return longitude


class FieldRainAvgListSerializer(FieldBaseSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)  # call the ModelSerializer.to_representation method.
        # add the "avg_milimeters" key with their value, to the representation dict.
        representation.update({"avg_milimeters": instance.avg_milimeters})
        return representation
