from django.urls import path

from smart_todo.tasks.views.add_task import AddTaskView

urlpatterns = [
    path("add", AddTaskView.as_view(), name="Create-Task"),
]
