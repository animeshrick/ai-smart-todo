from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.services.handlers.exception_handlers import ExceptionHandler
from tasks.services.task_service.task_service import TaskServices


class SearchTaskView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            query = request.query_params.get("q")  # free-text search
            status_filter = request.query_params.get("status")
            priority_filter = request.query_params.get("priority")

            result = TaskServices.search_task_service(
                query=query,
                status=status_filter,
                priority=priority_filter,
            )
            if result is None:
                return Response(
                    data={"message": "No data found for the given criteria."},
                    status=status.HTTP_404_NOT_FOUND,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "message": "Data is fetched`",
                        "data": result.model_dump(),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
