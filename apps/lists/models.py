from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class List(TimeStampedUUIDModel):
    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="lists"
    )
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=6)
        super().save(*args, **kwargs)
