import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from apps.lists.models import List
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskStatusSerializer

logger = logging.getLogger(__name__)


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        list_slug = self.kwargs.get("slug")
        list = get_object_or_404(List, slug=list_slug)
        if self.request.user != list.author:
            raise PermissionDenied("You do not have permission to view this list")
        return Task.objects.filter(list__slug=list_slug)


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        list_slug = self.kwargs.get("slug")
        list = get_object_or_404(List, slug=list_slug)
        user = self.request.user
        if user != list.author:
            raise PermissionDenied(
                "You do not have permission to create tasks in this list"
            )
        else:
            serializer.save(author=user, list=list)


class TaskDeleteAPIView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Task:
        list_slug = self.kwargs.get("slug")
        task_slug = self.kwargs.get("task_slug")
        list = get_object_or_404(List, slug=list_slug)
        try:
            task = Task.objects.get(list__slug=list_slug, slug=task_slug)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        user = self.request.user
        if user != list.author:
            logger.warning(
                f"Unauthorized delete attempt by user {user.username} on task {task.title}"
            )
            raise PermissionDenied("You do not have permission to delete this task")
        return task

    def delete(self, request, *args, **kwargs) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Task:
        list_slug = self.kwargs.get("slug")
        task_slug = self.kwargs.get("task_slug")
        list = get_object_or_404(List, slug=list_slug)
        try:
            task = Task.objects.get(list__slug=list_slug, slug=task_slug)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        if self.request.user != list.author:
            raise PermissionDenied("You do not have permission to update this task")
        return task

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TaskUpdateStatusAPIView(generics.UpdateAPIView):
    serializer_class = TaskStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Task:
        list_slug = self.kwargs.get("slug")
        task_slug = self.kwargs.get("task_slug")
        list = get_object_or_404(List, slug=list_slug)
        try:
            task = Task.objects.get(list__slug=list_slug, slug=task_slug)
        except Task.DoesNotExist:
            raise NotFound("Task not found")
        user = self.request.user
        if user != list.author:
            raise PermissionDenied(
                "You do not have permission to update this task's status"
            )
        return task

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.done is False:
            instance.done = True
        else:
            instance.done = False
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
