from random import randint, uniform
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import datetime, now, make_aware
from mixer.backend.django import mixer


from fields.models import Field
from rains.models import Rain


class UserFactory:
    @staticmethod
    def create_user(**kwargs):
        user = mixer.blend(User, **kwargs)
        return user


class FieldFactory:
    @staticmethod
    def create_field(**kwargs):
        owner = kwargs.get("owner")
        if owner is None:
            kwargs["owner"] = UserFactory.create_user()
        hectares = kwargs.get("hectares")
        if hectares is None:
            kwargs["hectares"] = uniform(1.0, 100000)
        latitude = kwargs.get("latitude")
        if latitude is None:
            kwargs["latitude"] = uniform(-90.0, 90.0)
        longitude = kwargs.get("longitude")
        if longitude is None:
            kwargs["longitude"] = uniform(-180.0, 180.0)
        field = mixer.blend(Field, **kwargs)
        return field

    @staticmethod
    def create_field_and_rains(**kwargs):
        field = FieldFactory.create_field(**kwargs)
        for _ in range(3, randint(5, 10)):
            RainFactory.create_rain(field=field)
        return field


class RainFactory:
    @staticmethod
    def create_rain(**kwargs):
        field = kwargs.get("field")
        if field is None:
            kwargs["field"] = FieldFactory.create_field()
        milimeters = kwargs.get("milimeters")
        if milimeters is None:
            kwargs["milimeters"] = uniform(0.1, 2000)
        rain_datetime = kwargs.get("rain_datetime")
        if rain_datetime is None:
            kwargs["rain_datetime"] = random_datetime_10_days_left_and_now()
        rain = mixer.blend(Rain, **kwargs)
        return rain


def random_datetime(first_datetime, second_datetime):
    """
    Returns random datetime between first_datetime and second_datetime.
    """

    if second_datetime < first_datetime:
        aux_datetime = first_datetime
        first_datetime = second_datetime
        second_datetime = aux_datetime
    first_timestamp = int(first_datetime.timestamp())
    second_timestamp = int(second_datetime.timestamp())
    random_timestamp = randint(first_timestamp, second_timestamp)
    naive_date_time = datetime.fromtimestamp(random_timestamp)
    date_time = make_aware(naive_date_time)
    return date_time


def random_datetime_10_days_left_and_now():
    """
    Returns random datetime string.
    """

    now_datetime = now()
    days = randint(0, 10)
    past_naive_datetime = datetime(now_datetime.year, now_datetime.month, now_datetime.day) - timedelta(days=days)
    past_datetime = make_aware(past_naive_datetime)
    return random_datetime(first_datetime=past_datetime, second_datetime=now_datetime)
