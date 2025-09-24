from django.core.management.base import BaseCommand
from missions.models import Mission, Target
from spy_cats.models import SpyCat
import random


class Command(BaseCommand):
    help = "Create test Missions with Targets"

    def handle(self, *args, **kwargs):
        cats = list(SpyCat.objects.all())
        if not cats:
            self.stdout.write(self.style.WARNING("No SpyCats found, create some first."))
            return

        for i in range(3):
            cat = random.choice(cats + [None])
            mission = Mission.objects.create(completed=False, cat=cat)
            for j in range(random.randint(1, 3)):
                Target.objects.create(
                    mission=mission,
                    name=f"Target {j+1} of Mission {mission.id}",
                    country=random.choice(["US", "FR", "UK"]),
                    notes="",
                    completed=False
                )
            self.stdout.write(self.style.SUCCESS(f"Created Mission #{mission.id} with targets"))
