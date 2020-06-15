from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import datetime

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from fields.models import Field
from rains.models import Rain
from utils.utils import FieldFactory, random_datetime_10_days_left_and_now, UserFactory


class RainCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create_user()
        self.field = FieldFactory.create_field(owner=self.user)
        date_time = random_datetime_10_days_left_and_now()
        self.request_data = {
            "field": self.field.id,
            "milimeters": 3423.322,
            "date_time": date_time.strftime("%Y-%m-%d, %H:%Mhs"),
        }
        self.client = APIClient()

    def _post_data(self, data):
        return self.client.post(reverse("rain_create"), data, format="json")

    def test_success(self):
        """
        Testing if a Rain is successfully created.
        """

        assert Field.objects.count() == 1
        assert Rain.objects.count() == 0
        response = self._post_data(data=self.request_data)
        assert Rain.objects.count() == 1
        data = response.data
        rain = Rain.objects.last()
        assert rain.field.id == data.get("field") == self.request_data.get("field")
        assert rain.milimeters == data.get("milimeters") == self.request_data.get("milimeters")
        rain_rain_datetime = rain.date_time.strftime("%Y-%m-%d, %H:%Mhs")
        data_rain_datetime = datetime.strptime(data.get("date_time"), "%Y-%m-%dT%H:%M:%SZ")
        data_rain_datetime = data_rain_datetime.strftime("%Y-%m-%d, %H:%Mhs")
        assert rain_rain_datetime == data_rain_datetime == self.request_data.get("date_time")
        assert rain.created is not None
        assert rain.updated is not None
        assert response.status_code == status.HTTP_201_CREATED

    def test_void_request_error(self):
        """
        Testing if a Rain is not created whit void request.data .
        """

        assert Field.objects.count() == 1
        assert Rain.objects.count() == 0
        response = self._post_data(data={})
        assert Rain.objects.count() == 0
        data = response.data
        assert data.get("field")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("milimeters")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("date_time")[0] == ErrorDetail(string="This field is required.", code="required")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_bad_request_error(self):
        """
        Testing if a Rain is not created whit bad values in request.data .
        """

        date_time = random_datetime_10_days_left_and_now() + timedelta(days=100)
        request_data = {
            "field": 666,
            "milimeters": -2000,
            "date_time": date_time.strftime("%Y-%m-%d, %H:%Mhs"),
        }
        assert Field.objects.count() == 1
        assert Rain.objects.count() == 0
        response = self._post_data(data=request_data)
        assert Rain.objects.count() == 0
        data = response.data

        assert data.get("field")[0] == ErrorDetail(
            string='Invalid pk "666" - object does not exist.', code="does_not_exist"
        )
        assert data.get("milimeters")[0] == ErrorDetail(
            string="milimeters must be 0 or positive value.", code="invalid"
        )
        assert data.get("date_time")[0] == ErrorDetail(
            string="date_time must be a past datetime.", code="invalid"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_incomplete_rain_date_time_error(self):
        """
        Testing if a Rain is not created whit incomplete date_time in request.data .
        """

        date_time = random_datetime_10_days_left_and_now()
        self.request_data.update({"date_time": date_time.strftime("%Y-%m-%d")})
        assert Field.objects.count() == 1
        assert Rain.objects.count() == 0
        response = self._post_data(data=self.request_data)
        assert Rain.objects.count() == 0
        data = response.data
        assert data.get("date_time")[0] == ErrorDetail(
            string="Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].",
            code="invalid",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
