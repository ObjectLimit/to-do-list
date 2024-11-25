from django.urls import path

from ..tasks.views import (
    TaskCreateAPIView,
    TaskDeleteAPIView,
    TaskListAPIView,
    TaskUpdateAPIView,
    TaskUpdateStatusAPIView,
)
from .views import (
    ListCreateAPIView,
    ListDeleteAPIView,
    ListUpdateAPIView,
    MyListsAPIView,
)

urlpatterns = [
    path("all/", MyListsAPIView.as_view(), name="list-all"),
    path("create/", ListCreateAPIView.as_view(), name="list-create"),
    path("<slug:slug>/delete/", ListDeleteAPIView.as_view(), name="list-delete"),
    path("<slug:slug>/update/", ListUpdateAPIView.as_view(), name="list-update"),
    path("<slug:slug>/", TaskListAPIView.as_view(), name="tasks"),
    path("<slug:slug>/task/", TaskCreateAPIView.as_view(), name="task-create"),
    path(
        "<slug:slug>/task/<slug:task_slug>/delete/",
        TaskDeleteAPIView.as_view(),
        name="task-delete",
    ),
    path(
        "<slug:slug>/task/<slug:task_slug>/update/",
        TaskUpdateAPIView.as_view(),
        name="task-update",
    ),
    path(
        "<slug:slug>/task/<slug:task_slug>/status/",
        TaskUpdateStatusAPIView.as_view(),
        name="task-status",
    ),
]
