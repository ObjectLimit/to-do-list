from uuid import UUID

import cloudinary
from celery import shared_task

from apps.profiles.models import Profile


@shared_task(name="upload_avatar_to_cloudinary")
def upload_avatar_to_cloudinary(profile_id: UUID, image_content: bytes) -> None:
    profile = Profile.objects.get(id=profile_id)
    response = cloudinary.uploader.upload(image_content)
    profile.avatar = response["url"]
    profile.save()
