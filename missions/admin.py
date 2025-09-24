from django.contrib import admin
from .models import Mission, Target


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """
    Admin interface for Mission model.
    """
    list_display = ['id', 'cat', 'completed']
    list_filter = ['cat', 'completed']


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    """
    Admin interface for Target model.
    """
    list_display = ['id', 'mission', 'name', 'completed', 'notes', 'country']
    list_filter = ['mission', 'completed', 'country']
    search_fields = ['name', 'notes']
