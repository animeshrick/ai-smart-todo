from typing import Optional

from rest_framework import serializers

from tasks.models.model.task_model import Task
from tasks.services.helpers import validate_string_input, validate_dateTime_input, validate_list_input
from tasks.export_types.request_data_types.add_task import AddTaskRequestType


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: AddTaskRequestType = data.get("request_data")

        if not request:
            raise serializers.ValidationError(detail="Request data is required.")

        if not request.title and validate_string_input(request.title):
            raise serializers.ValidationError(detail="Title should not be empty.")

        if not request.description and validate_string_input(request.description):
            raise serializers.ValidationError(detail="Description should not be empty.")

        if not request.category and validate_string_input(request.category):
            raise serializers.ValidationError(detail="Category should not be empty.")

        # validate date
        if not request.due_date and validate_dateTime_input(request.due_date):
            raise serializers.ValidationError(detail="Due date should not be empty.")

        # validate date
        if not request.completed_at and validate_dateTime_input(request.completed_at):
            raise serializers.ValidationError(detail="Completed date should not be empty.")

        # "tags": ["personal", "shopping", "errand"]
        if not request.tags and validate_list_input(request.tags):
            raise serializers.ValidationError(detail="Tags should be a list.")

        for tag in request.tags:
            if not validate_string_input(tag):
                raise serializers.ValidationError(detail="Tag should not be empty and must be a string.")

        return True

    def create(self, data: dict) -> Task:
        if self.validate(data):
            request: AddTaskRequestType = data.get("request_data")
            # create or update a task object
            task = Task.objects.get_or_create(
                title=request.title,
                description=request.description,
                category=request.category,
                due_date=request.due_date,
                completed_at=request.completed_at,
                tags=request.tags,
                is_active=True,
            )
            return task
