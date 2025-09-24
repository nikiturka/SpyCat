from rest_framework import generics

from .models import Mission, Target
from .serializers import (
    CreateMissionSerializer,
    DetailMissionSerializer,
    UpdateMissionSerializer,
    UpdateTargetSerializer,
    DetailTargetSerializer
)


class MissionListCreateAPIView(generics.ListCreateAPIView):
    """
    APIView for listing and creating Mission objects.
    """
    def get_queryset(self):
        return Mission.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateMissionSerializer
        return DetailMissionSerializer


class MissionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView for retrieving and updating Mission object.
    """
    def get_queryset(self):
        return Mission.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateMissionSerializer
        return DetailMissionSerializer


class TargetUpdateAPIView(generics.UpdateAPIView):
    """
    APIView for updating Target objects.
    """
    def get_queryset(self):
        return Target.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateTargetSerializer
        return DetailTargetSerializer
