from django.urls import path

from tasks.views.add_task import AddTaskView
from tasks.views.archive_task import ArchiveTaskView
from tasks.views.edit_task import EditTaskView
from tasks.views.search_task import SearchTaskView
from tasks.views.view_task import ViewTaskView

urlpatterns = [
    path("add", AddTaskView.as_view(), name="Create-Task"),
    path("update", EditTaskView.as_view(), name="Edit-Task"),
    path("read", ViewTaskView.as_view(), name="View-Task"),
    path("archive", ArchiveTaskView.as_view(), name="Archive-Task"),
    path("search", SearchTaskView.as_view(), name="Search-Task"),
]
