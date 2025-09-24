from rest_framework import serializers

from .models import SpyCat


class SpyCatPrimaryKeyField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return SpyCat.objects.all()
