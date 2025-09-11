from django.urls import path

from tasks.views.add_task import AddTaskView
from tasks.views.edit_task import EditTaskView
from tasks.views.view_task import ViewTaskView

urlpatterns = [
    path("add", AddTaskView.as_view(), name="Create-Task"),
    path("update", EditTaskView.as_view(), name="Edit-Task"),
    path("read", ViewTaskView.as_view(), name="View-Task"),
]
