from django.db import models
from rest_framework.exceptions import ValidationError

from spy_cats.models import SpyCat
from .managers import MissionManager


class Mission(models.Model):
    cat = models.ForeignKey(SpyCat, on_delete=models.SET_NULL, related_name="mission_cat", null=True)
    completed = models.BooleanField(default=False)

    objects = MissionManager()

    def __str__(self):
        return f"Mission #{self.id}"

    def delete(self, *args, **kwargs):
        if self.cat is not None:
            raise ValidationError("Cannot delete a mission that has a cat assigned.")
        super().delete(*args, **kwargs)


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="target_mission")
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Target #{self.id} for mission {self.mission_id}"
