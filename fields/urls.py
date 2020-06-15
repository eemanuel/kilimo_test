from django.urls import path
from fields import views

urlpatterns = [
    path("rain_avg_list/", views.FieldRainAvgListAPIView.as_view(), name="fields_rain_avg_list"),
    path(
        "accomulated_rain_list/",
        views.FieldAccumulatedRainListAPIView.as_view(),
        name="fields_accomulated_rain_list",
    ),
    path("<int:pk>/all_rain/", views.FieldAllRainListAPIView.as_view(), name="fields_all_rain_list"),
    path("create/", views.FieldsCreateAPIView.as_view(), name="fields_create"),
]
