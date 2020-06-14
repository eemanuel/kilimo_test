from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import datetime, now, make_aware

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ErrorDetail

from fields.models import Field
from utils.utils import FieldFactory, UserFactory


class FieldsCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create_user()
        self.request_data = {
            "owner": self.user.id,
            "name": "La Comarca",
            "hectares": 1750.3,
            "latitude": -32.167455,
            "longitude": -62.364923,
        }
        self.client = APIClient()

    def _post_data(self, data):
        return self.client.post(reverse("fields_create"), data, format="json")

    def test_success(self):
        """
        Testing if a Field is successfully created.
        """

        assert Field.objects.count() == 0
        response = self._post_data(data=self.request_data)
        assert Field.objects.count() == 1
        data = response.data
        field = Field.objects.last()
        assert field.name == data.get("name") == self.request_data.get("name")
        assert field.hectares == data.get("hectares") == self.request_data.get("hectares")
        assert float(field.latitude) == float(data.get("latitude")) == self.request_data.get("latitude")
        assert float(field.longitude) == float(data.get("longitude")) == self.request_data.get("longitude")
        assert field.created is not None
        assert field.updated is not None
        assert response.status_code == status.HTTP_201_CREATED

    def test_void_request_error(self):
        """
        Testing if a Field is not created whit void request.data .
        """

        assert Field.objects.count() == 0
        response = self._post_data(data={})
        assert Field.objects.count() == 0
        data = response.data
        assert data.get("owner")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("name")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("hectares")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("latitude")[0] == ErrorDetail(string="This field is required.", code="required")
        assert data.get("longitude")[0] == ErrorDetail(string="This field is required.", code="required")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_bad_request_error(self):
        """
        Testing if a Field is not created whit bad values in request.data .
        """

        assert Field.objects.count() == 0
        request_data = {
            "owner": 666,
            "name": "The name of this field is the name that first old man owner.",
            "hectares": -100,
            "latitude": 120.44,
            "longitude": 100.3649235435437765,
        }
        response = self._post_data(data=request_data)
        assert Field.objects.count() == 0
        data = response.data
        assert data.get("owner")[0] == ErrorDetail(
            string='Invalid pk "666" - object does not exist.', code="does_not_exist"
        )
        assert data.get("name")[0] == ErrorDetail(
            string="Ensure this field has no more than 20 characters.", code="max_length"
        )
        assert data.get("hectares")[0] == ErrorDetail(string="hectares must be positive.", code="invalid")
        assert data.get("latitude")[0] == ErrorDetail(
            string="Ensure that there are no more than 2 digits before the decimal point.", code="max_whole_digits"
        )
        assert data.get("longitude")[0] == ErrorDetail(
            string="Ensure that there are no more than 9 digits in total.", code="max_digits"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class FieldRainAvgListAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory.create_user()
        self._create_fields_and_rains()
        self.queryparams = {"last_days": 5}
        self.client = APIClient()

    def _get_data(self, queryparams):
        return self.client.get(reverse("fields_rain_avg_list"), queryparams)

    def _create_fields_and_rains(self):
        for _ in range(5):
            FieldFactory.create_field_and_rains(owner=self.user)

    def test_success(self):
        """
        Testing if all fields are successfully listed whith the rain's milimeters average
        at the last 'last_days' days.
        """

        response = self._get_data(queryparams=self.queryparams)
        data = response.data

        last_days_int = self.queryparams.get("last_days")
        now_datetime = now()
        now_datetime_ymd = datetime(now_datetime.year, now_datetime.month, now_datetime.day)
        last_days_naive = now_datetime_ymd - timedelta(days=last_days_int)
        last_days = make_aware(last_days_naive)
        for field_dict in data:
            id_value = field_dict.get("id")
            field = Field.objects.get(id=id_value)
            rain_dicts_qs = field.rain.filter(rain_datetime__gte=last_days).values("milimeters")
            milimeters_list = []
            for rain_dict in rain_dicts_qs:
                milimeters = rain_dict.get("milimeters")
                milimeters_list.append(milimeters)
            milimeters_list_avg = sum(milimeters_list) / len(milimeters_list)
            assert round(milimeters_list_avg, 5) == round(field_dict.get("avg_milimeters"), 5)
            assert field_dict.get("owner") is not None
            assert field_dict.get("name") is not None
            assert field_dict.get("hectares") is not None
            assert field_dict.get("latitude") is not None
            assert field_dict.get("longitude") is not None
        assert response.status_code == status.HTTP_200_OK

    def test_void_queryparams_succes(self):
        """
        Testing if view return [] whit void queryparams.
        """

        response = self._get_data(queryparams={})
        data = response.data
        assert data == []
        assert response.status_code == status.HTTP_200_OK

    def test_big_value_queryparams_succes(self):
        """
        Testing if view return [] whit big value in queryparams.
        """

        response = self._get_data(queryparams={"last_days": 8})
        data = response.data
        assert data == []
        assert response.status_code == status.HTTP_200_OK

    def test_negative_value_queryparams_succes(self):
        """
        Testing if view return [] whit negative value in queryparams.
        """

        response = self._get_data(queryparams={"last_days": -1})
        data = response.data
        assert data == []
        assert response.status_code == status.HTTP_200_OK

