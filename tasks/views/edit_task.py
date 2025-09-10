from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.export_types.request_data_types.edit_task import EditTaskRequestType
from tasks.services.handlers.exception_handlers import ExceptionHandler
from tasks.services.task_service.task_service import TaskServices


class EditTaskView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            result = TaskServices.edit_task_service(
                request_data=EditTaskRequestType(**request.data)
            )
            return Response(
                data={
                    "message": "Task is updated.",
                    "data": result.model_dump(),
                },
                status=status.HTTP_201_CREATED,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
