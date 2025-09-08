from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from smart_todo.tasks.export_types.request_data_types.add_task import AddTaskRequestType
from smart_todo.tasks.services.handlers.exception_handlers import ExceptionHandler
from smart_todo.tasks.services.task_service.task_service import TaskServices


class AddTaskView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            result = TaskServices.create_new_task_service(
                request_data=AddTaskRequestType(**request.data)
            )
            return Response(
                data={
                    "message": (result.get("message")),
                    "data": result.get("data"),
                },
                status=status.HTTP_201_CREATED,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)