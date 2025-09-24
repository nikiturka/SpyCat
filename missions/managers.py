from django.db import models
from django.db.models import Prefetch


class MissionManager(models.Manager):
    def get_queryset(self):
        from .models import Target
        return super().get_queryset().select_related(
            'cat'
        ).prefetch_related(
            Prefetch(
                'target_mission',
                queryset=Target.objects.all(),
                to_attr='targets'
            )
        )
