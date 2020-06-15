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
        if last_days_int not in range(7):
            return Field.objects.none()
        # create last_days aware datetime.
        now_datetime = now()
        now_datetime_ymd = datetime(now_datetime.year, now_datetime.month, now_datetime.day)
        last_days_naive = now_datetime_ymd - timedelta(days=last_days_int)
        last_days = make_aware(last_days_naive)
        # make the queryset and return it.
        queryset = Field.objects.annotate(
            avg_milimeters=Avg(
                Case(When(rains__date_time__gte=last_days, then="rains__milimeters"), output_field=FloatField())
            )
        ).order_by("id")
        return queryset


class FieldAccumulatedRainListAPIView(ListAPIView):
    """
    Lists all fields whit their total rain as long
    the total rain is grater than 'accumulated_rain_gt' value.
    """

    serializer_class = FieldSerializer

    def get_queryset(self):
        accumulated_rain_gt = self.request.query_params.get("accumulated_rain_gt")
        # check accumulated_rain_gt.
        if accumulated_rain_gt is None:
            return Field.objects.none()
        accumulated_rain = float(accumulated_rain_gt)
        if accumulated_rain < 0:
            return Field.objects.none()
        # make the queryset and return it.
        queryset = (
            Field.objects.annotate(accumulated_rain=Sum("rains__milimeters"))
            .filter(accumulated_rain__gt=accumulated_rain)
            .order_by("id")
        )
        return queryset


class FieldAllRainListAPIView(ListAPIView):
    """
    Lists all fields as long the total rain is grater than 'accumulated_rain_gt' value.
    """

    serializer_class = RainSerializer

    # Use __init__ when you need to control initialization of a new instance.
    def __init__(self, **kwargs):
        self.field_model = None  # define field_model as class variable.
        super().__init__(**kwargs)  # call the ListAPIView.__init__ method.

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        # try overwrite self.field_model.
        try:
            self.field_model = Field.objects.get(id=pk)
        except Field.DoesNotExist:
            return Response(f"Field id={pk} doesn't exist.", status=status.HTTP_400_BAD_REQUEST)
        return super().get(self, request, *args, **kwargs)  # call the ListAPIView.get method.

    def get_queryset(self):
        return self.field_model.rains.all()
