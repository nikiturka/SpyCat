import requests
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import SpyCat


class BaseSpyCatSerializer(serializers.ModelSerializer):
    """
    Base Serializer class for SpyCat model.
    """
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'salary', 'breed', 'years_of_experience']


class UpdateSpyCatSerializer(serializers.ModelSerializer):
    """
    Serializer class for updating SpyCat objects.
    """
    default_error_messages = {
        "negative_salary": _("Salary must be greater than 0."),
    }

    class Meta:
        model = SpyCat
        fields = ['salary']

    def validate_salary(self, value):
        if value <= 0:
            self.fail("negative_salary")
        return value


class CreateSpyCatSerializer(UpdateSpyCatSerializer):
    """
    Serializer class for creating SpyCat objects with additional validation.
    """
    default_error_messages = {
        "breed_not_found": _("Breed '{value}' not found in TheCatAPI."),
        "breed_api_failed": _("Failed to validate breed with TheCatAPI."),
    }

    class Meta:
        model = SpyCat
        fields = BaseSpyCatSerializer.Meta.fields

    def validate_breed(self, value):
        try:
            response = requests.get("https://api.thecatapi.com/v1/breeds")
            response.raise_for_status()
            breeds = [breed["name"].lower() for breed in response.json()]
            if value.lower() not in breeds:
                self.fail("breed_not_found", value=value)
        except requests.RequestException:
            self.fail("breed_api_failed")
        return value
