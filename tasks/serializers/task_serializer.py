from typing import Optional

from rest_framework import serializers

from ai_module.ai_services.auto_assign_task_tag import extract_tags_from_text
from ai_module.ai_services.auto_categorize_task import auto_categorize_task
from ai_module.ai_services.smart_priority_assignment import smart_priority_assignment
from tasks.models.model.task_model import Task
from tasks.services.helpers import (
    validate_string_input,
    validate_dateTime_input,
    validate_list_input,
    convert_string_to_dateTime,
)
from tasks.export_types.request_data_types.add_task import AddTaskRequestType


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: AddTaskRequestType = data.get("request_data")

        if request.category and not validate_string_input(request.category):
            raise serializers.ValidationError(detail="Category should not be empty.")

        if request.due_date and not validate_dateTime_input(request.due_date):
                raise serializers.ValidationError(detail="Due date should not be empty.")

        if request.completed_at and not validate_dateTime_input(request.completed_at):
            raise serializers.ValidationError(
                detail="Completed date should not be empty."
            )

        if request.priority and not validate_string_input(request.priority):
            raise serializers.ValidationError(
                detail="Priority should not."
            )

        if request.tags and not validate_list_input(request.tags):
            raise serializers.ValidationError(
                detail="Tags should not be empty and must be a list."
            )

        if validate_list_input(request.tags):
            for tag in request.tags:
                if not validate_string_input(tag):
                    raise serializers.ValidationError(
                        detail="Tag should not be empty and must be a string."
                    )

        return True

    def create(self, data: dict) -> Optional[Task]:
        if self.validate(data):
            request: AddTaskRequestType = data.get("request_data")

            due_date = convert_string_to_dateTime(request.due_date)
            completed_at = convert_string_to_dateTime(request.completed_at)
            tag_list = request.tags
            tag_string_list = ""

            if not tag_list:
                ai_tags: str = extract_tags_from_text(request.title, request.description)
                print(f"Onion_ai_tags: {ai_tags}")

                tag_string_list = ai_tags
            else:
                if validate_list_input(tag_list):
                    for tag in tag_list:
                        tag_string_list += tag + ","

            if not request.category:
                ai_category = auto_categorize_task(request.title, request.description)
                print(f"Onion_ai_category: {ai_category}")

                request.category = ai_category

            if not request.priority:
                ai_priority = smart_priority_assignment(request.title, request.description, due_date)
                print(f"Onion_ai_priority: {ai_priority}")
                request.priority = ai_priority


            task = Task.objects.create(
                title=request.title,
                description=request.description,
                category=request.category,
                due_date=due_date,
                completed_at=completed_at,
                tags=tag_string_list,
                priority=request.priority,
                is_active=True,
            )
            return task
        return None