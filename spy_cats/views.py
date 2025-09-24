from rest_framework import generics
from rest_framework.generics import get_object_or_404

from .models import SpyCat
from .serializers import BaseSpyCatSerializer, CreateSpyCatSerializer, UpdateSpyCatSerializer


class SpyCatListCreateAPIView(generics.ListCreateAPIView):
    """
    APIView for listing all Spy Cats or creating a new one
    """
    serializer_class = CreateSpyCatSerializer

    def get_queryset(self):
        return SpyCat.objects.all()


class SpyCatRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView for retrieving and updating Spy Cat instances.
    """
    http_method_names = ["get", "patch", "delete"]

    def get_object(self):
        return get_object_or_404(SpyCat, pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateSpyCatSerializer
        return BaseSpyCatSerializer
