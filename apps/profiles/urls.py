from django.urls import path

from apps.profiles.views import AvatarUploadView, ProfileDetailAPIView

urlpatterns = [
    path("me/", ProfileDetailAPIView.as_view(), name="profile-me"),
    path("avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]
