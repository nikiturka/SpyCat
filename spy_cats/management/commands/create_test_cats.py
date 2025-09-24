from django.core.management.base import BaseCommand
from spy_cats.models import SpyCat
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Create test SpyCats"

    def handle(self, *args, **kwargs):
        breeds = ["Siamese", "Persian", "Maine Coon", "Bengal"]
        for i in range(5):
            cat = SpyCat.objects.create(
                name=f"Cat{i+1}",
                years_of_experience=random.randint(1, 10),
                breed=random.choice(breeds),
                salary=Decimal(random.randint(500, 2000))
            )
            self.stdout.write(self.style.SUCCESS(f"Created SpyCat: {cat.name}"))
