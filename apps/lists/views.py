import logging

from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.lists.models import List
from apps.lists.serializers import ListSerializer

logger = logging.getLogger(__name__)
User = get_user_model()


class MyListsAPIView(generics.ListAPIView):
    serializer_class = ListSerializer

    def get_queryset(self):
        return List.objects.filter(author=self.request.user).order_by("-created_at")


class ListCreateAPIView(generics.CreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


class ListDeleteAPIView(generics.DestroyAPIView):
    queryset = List.objects.all()
    lookup_field = "slug"
    serializer_class = ListSerializer

    def get_object(self) -> List:
        try:
            list = super().get_object()
        except Http404:
            raise Http404("List not found")
        user = self.request.user
        if user != list.author:
            logger.warning(
                f"Unauthorized delete attempt by user {user.username} on list {list.title}"
            )
            raise PermissionDenied("You do not have permission to delete this list")
        return list

    def delete(self, request, *args, **kwargs) -> Response:
        super().delete(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListUpdateAPIView(generics.UpdateAPIView):
    queryset = List.objects.all()
    lookup_field = "slug"
    serializer_class = ListSerializer

    def get_object(self) -> List:
        try:
            list = super().get_object()
        except Http404:
            raise Http404("List not found")
        user = self.request.user
        if user != list.author:
            raise PermissionDenied("You do not have permission to update this list")
        return list

    def perform_update(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
