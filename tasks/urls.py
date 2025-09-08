from django.urls import path

from tasks.views.add_task import AddTaskView

urlpatterns = [
    path("add", AddTaskView.as_view(), name="Create-Task"),
]
