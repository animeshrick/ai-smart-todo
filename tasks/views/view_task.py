from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.export_types.request_data_types.edit_task import EditTaskRequestType
from tasks.services.handlers.exception_handlers import ExceptionHandler
from tasks.services.task_service.task_service import TaskServices


class ViewTaskView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            result = TaskServices.view_task_service(
                task_id=request.data.get("id")
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
