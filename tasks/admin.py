from django.contrib import admin

from tasks.models.model.task_model import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "priority", "category", "due_date", "is_active", "created_at")
    list_filter = ("status", "priority", "category", "is_active", "due_date")
    search_fields = ("title", "description", "tags")
    list_editable = ("status", "priority", "category", "is_active")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("title", "description", "tags")
        }),
        ("Status and Priority", {
            "fields": ("status", "priority", "category")
        }),
        ("Dates", {
            "fields": ("due_date", "completed_at")
        }),
        ("Activation", {
            "fields": ("is_active",)
        }),
    )

    readonly_fields = ("created_at", "updated_at")
