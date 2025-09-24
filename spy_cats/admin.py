from django.contrib import admin

from .models import SpyCat


@admin.register(SpyCat)
class SpyCatAdmin(admin.ModelAdmin):
    """
    Admin interface for SpyCat model.
    """
    list_display = ['id', 'name', 'breed', 'years_of_experience', 'salary']
    search_fields = ['name']
    list_filter = ['years_of_experience', 'breed']
    ordering = ['id', 'years_of_experience', 'salary']
