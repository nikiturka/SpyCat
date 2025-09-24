from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'SpyCat {self.id}: {self.name}'

    class Meta:
        verbose_name = 'Spy Cat'
        verbose_name_plural = 'Spy Cats'
