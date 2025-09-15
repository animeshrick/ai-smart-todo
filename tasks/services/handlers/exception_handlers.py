import logging
from sqlite3 import DatabaseError

import django
from rest_framework import status, serializers
from pydantic import ValidationError
from rest_framework.response import Response


class ExceptionHandler:
    @staticmethod
    def get_handlers(self) -> dict:
        return {
            DatabaseError: {
                "message": "DatabaseError: Error Occured While Fetching details from database",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            ValidationError: {
                "message": "PydanticValidationError: Error Occured while converting to Pydantic object",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            NotImplementedError: {
                "message": "NotImplementedError",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            ValueError: {
                "message": "ValueError",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
            serializers.ValidationError: {
                "message": "SerializerValidationError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            django.core.exceptions.ValidationError: {
                "message": "ValidationError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
        }

    def handle_exception(self, e: Exception):
        handlers = self.get_handlers()
        for exc_type, handler in handlers.items():
            if isinstance(e, exc_type):
                logging.error(
                    f"{handler['message']}: {e.msg}"
                    if hasattr(e, "msg")
                    else f"{handler['message']}: {str(e)}"
                )
                if isinstance(e, serializers.ValidationError):
                    e.msg = "; ".join([error for error in e.detail])
                return Response(
                    data={
                        "message": (
                            f"{handler['message']}: {e.msg}"
                            if hasattr(e, "msg")
                            else f"{handler['message']}: {str(e)}"
                        ),
                    },
                    status=handler["status"],
                    content_type="application/json",
                )
        else:
            logging.error(f"InternalServerError: {e}")
            raise e
