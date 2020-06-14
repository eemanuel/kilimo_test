from datetime import timedelta

from django.db.models import Avg, Case, FloatField, Sum, When
from django.utils.timezone import datetime, now, make_aware

from fields.models import Field
from fields.serializers import FieldSerializer, FieldRainAvgListSerializer
from rains.serializers import RainSerializer

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status


class FieldsCreateAPIView(CreateAPIView):
    """
    Create a Field model instance.
    """

    serializer_class = FieldSerializer


class FieldRainAvgListAPIView(ListAPIView):
    """
    Lists all fields whit their rain average in the last 'last_days' days.
    """

    serializer_class = FieldRainAvgListSerializer

    def get_queryset(self):
        last_days_query_param = self.request.query_params.get("last_days")
        # check last_days_query_param.
        if last_days_query_param is None:
            return Field.objects.none()
        last_days_int = int(last_days_query_param)
        if last_days_int < 0 or 7 < last_days_int:
            return Field.objects.none()
        # create last_days aware datetime.
        now_datetime = now()
        now_datetime_ymd = datetime(now_datetime.year, now_datetime.month, now_datetime.day)
        last_days_naive = now_datetime_ymd - timedelta(days=last_days_int)
        last_days = make_aware(last_days_naive)
        # make the queryset and return it.
        queryset = Field.objects.annotate(
            avg_milimeters=Avg(
                Case(When(rain__rain_datetime__gte=last_days, then="rain__milimeters"), output_field=FloatField())
            )
        ).order_by("id")
        return queryset

