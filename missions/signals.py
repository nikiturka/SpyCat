from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Target


@receiver(post_save, sender=Target)
def mark_mission_completed(sender, instance, **kwargs):
    """
    Mark mission as completed if all its targets completed.
    """
    mission = instance.mission
    if mission.target_mission.filter(completed=False).count() == 0:
        mission.completed = True
        mission.save()
