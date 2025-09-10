from django.urls import path

from tasks.views.add_task import AddTaskView
from tasks.views.edit_task import EditTaskView

urlpatterns = [
    path("add", AddTaskView.as_view(), name="Create-Task"),
    path("update", EditTaskView.as_view(), name="Edit-Task"),
]
