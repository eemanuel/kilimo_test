from django.urls import path
from rains import views

urlpatterns = [path("create/", views.RainCreateAPIView.as_view(), name="rain_create")]
