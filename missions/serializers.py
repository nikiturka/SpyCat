from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from spy_cats.relations import SpyCatPrimaryKeyField
from spy_cats.serializers import BaseSpyCatSerializer
from .models import Target, Mission


class BaseTargetSerializer(serializers.ModelSerializer):
    """
    Base Serializer class for Target objects.
    """

    class Meta:
        model = Target
        fields = ['id', 'notes', 'completed']


class UpdateTargetSerializer(serializers.ModelSerializer):
    """
    Serializer class for updating Target objects.
    """
    default_error_messages = {
        "target_or_mission_completed": _("Cannot update notes because this target or its mission is completed.")
    }

    class Meta:
        model = Target
        fields = BaseTargetSerializer.Meta.fields

    def validate_notes(self, value):
        target = self.instance
        if target.completed or target.mission.completed:
            self.fail("target_or_mission_completed")
        return value


class DetailTargetSerializer(BaseTargetSerializer):
    """
    Detail Serializer class for Target objects with additional fields.
    """
    class Meta:
        model = Target
        fields = BaseTargetSerializer.Meta.fields + ['country', 'name']


class BaseMissionSerializer(serializers.ModelSerializer):
    """
    Base Serializer class for Mission objects.
    """

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'completed']


class CreateMissionSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating Mission objects with nested targets and additional validation.
    """
    default_error_messages = {
        "invalid_target_number": _("Mission should contain from 1 to 3 targets."),
    }

    targets = BaseTargetSerializer(many=True, write_only=True)

    class Meta:
        model = Mission
        fields = BaseMissionSerializer.Meta.fields + ['targets']

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            self.fail("invalid_target_number")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class DetailMissionSerializer(serializers.ModelSerializer):
    """
    Detail serializer class for Mission objects with nested objects.
    """
    targets = DetailTargetSerializer(many=True, read_only=True)
    cat = BaseSpyCatSerializer(read_only=True)

    class Meta:
        model = Mission
        fields = BaseMissionSerializer.Meta.fields + ['targets', 'cat']


class UpdateMissionSerializer(serializers.ModelSerializer):
    """
    Serializer class for assigning a SpyCat to a Mission.
    """
    default_error_messages = {
        "cat_mission_exists": _("This Spy Cat already has an active mission."),
    }

    cat = SpyCatPrimaryKeyField(allow_null=True)

    class Meta:
        model = Mission
        fields = ['cat']

    def validate_cat(self, value):
        if value is None:
            return value

        active_missions = Mission.objects.filter(cat=value, completed=False)
        if self.instance:
            active_missions = active_missions.exclude(pk=self.instance.pk)

        if active_missions.exists():
            self.fail("cat_mission_exists")
        return value
