from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class List(TimeStampedUUIDModel):
    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="lists"
    )
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")
