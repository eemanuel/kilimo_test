from rains.serializers import RainSerializer

from rest_framework.generics import CreateAPIView


class RainCreateAPIView(CreateAPIView):
    """
    Create a Rain model instance.
    """

    serializer_class = RainSerializer
