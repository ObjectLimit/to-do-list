from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = CloudinaryField(verbose_name=_("Avatar"), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
