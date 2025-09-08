from smart_todo.tasks.export_types.request_data_types.add_task import AddTaskRequestType
from smart_todo.tasks.export_types.task_export_types.export_task import ExportTask
from smart_todo.tasks.models.model.task_model import Task

from smart_todo.tasks.serializers.task_serializer import TaskSerializer


class TaskServices:
    @staticmethod
    def create_new_task_service(request_data: AddTaskRequestType) -> dict:
        data: dict = {"request_data": request_data}
        task: Task = TaskSerializer().create(data)
        return {
            "message": f"{task.title} is created",
            "data": ExportTask(**task.model_to_dict()).model_dump(),
        }
