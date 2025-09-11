from tasks.export_types.request_data_types.add_task import AddTaskRequestType
from tasks.export_types.request_data_types.edit_task import EditTaskRequestType
from tasks.export_types.task_export_types.export_task import ExportTask
from tasks.models.model.task_model import Task
from tasks.serializers.task_serializer import TaskSerializer
from tasks.services.const import STATUS_CHOICES, PRIORITY_CHOICES
from tasks.services.helpers import (
    validate_string_input,
    suggest_closest,
    validate_list_input,
    validate_boolean_input,
    convert_dateTime_to_string,
    convert_string_to_dateTime,
)
from django.utils import timezone


class TaskServices:
    @staticmethod
    def create_new_task_service(request_data: AddTaskRequestType) -> dict:
        data: dict = {"request_data": request_data}
        task: Task = TaskSerializer().create(data)
        return {
            "message": f"{task.title} is created",
            "data": ExportTask(**task.model_to_dict()).model_dump(),
        }

    @staticmethod
    def edit_task_service(request_data: EditTaskRequestType) -> ExportTask:
        if not validate_string_input(request_data.id):
            raise ValueError("Id is required")
        try:
            task = Task.objects.get(id=request_data.id, is_active=True)
        except Exception:
            raise ValueError("No task exists")

        if (
            validate_string_input(request_data.description)
            and request_data.description != task.description
        ):
            task.description = request_data.description

        # validate & update status, priority
        if validate_string_input(request_data.status):
            if request_data.status not in STATUS_CHOICES:
                suggestion = suggest_closest(request_data.status, STATUS_CHOICES)
                msg = f"Invalid status value: '{request_data.status}'. Must be one of {STATUS_CHOICES}."
                if suggestion:
                    msg += f" Did you mean '{suggestion}'?"
                raise ValueError(msg)
            else:
                if request_data.status.lower() == "completed":
                    task.completed_at = timezone.now()
                task.status = request_data.status

        if validate_string_input(request_data.priority):
            if request_data.priority not in PRIORITY_CHOICES:
                suggestion = suggest_closest(request_data.priority, PRIORITY_CHOICES)
                msg = f"Invalid priority value: '{request_data.priority}'. Must be one of {PRIORITY_CHOICES}."
                if suggestion:
                    msg += f" Did you mean '{suggestion}'?"
                raise ValueError(msg)
            else:
                task.priority = request_data.priority

        # validate & update category
        if (
            validate_string_input(request_data.category)
            and request_data.category != task.category
        ):
            task.category = request_data.category

        # validate & update tags
        # if validate_list_input(request_data.tags) and request_data.tags != task.tags:
        #     task.tags = request_data.tags

        if validate_list_input(request_data.tags):
            for tag in request_data.tags:
                if tag in task.tags:
                    request_data.tags.remove(tag)
                else:
                    task.tags += tag + ","

        # validate & update due date
        if validate_string_input(
            request_data.due_date
        ) and request_data.due_date != convert_dateTime_to_string(task.due_date):
            task.due_date = convert_string_to_dateTime(request_data.due_date)

        # validate & update complete date
        if validate_string_input(
            request_data.completed_at
        ) and request_data.completed_at != convert_dateTime_to_string(
            task.completed_at
        ):
            task.completed_at = convert_string_to_dateTime(request_data.completed_at)

        # validate & update isActive
        if (
            validate_boolean_input(request_data.is_active)
            and request_data.is_active != task.is_active
        ):
            task.is_active = request_data.is_active

        task.updated_at = timezone.now()
        task.save()
        return ExportTask(**task.model_to_dict())
