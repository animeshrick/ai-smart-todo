from django.contrib import admin

from tasks.models.model.task_model import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "updated_at")
    readonly_fields = ("created_at", "updated_at")
