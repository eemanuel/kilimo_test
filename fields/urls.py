from django.urls import path
from fields import views

urlpatterns = [
    path("field/rain_avg_list/", views.FieldRainAvgListAPIView.as_view(), name="fields_rain_avg_list"),
    path(
        "field/accomulated_rain_list/",
        views.FieldAccumulatedRainListAPIView.as_view(),
        name="fields_accomulated_rain_list",
    ),
    path("field/<int:pk>/all_rain/", views.FieldAllRainListAPIView.as_view(), name="fields_all_rain_list"),
    path("field/create/", views.FieldsCreateAPIView.as_view(), name="fields_create"),
]
