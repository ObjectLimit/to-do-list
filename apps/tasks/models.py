from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.common.utils import generate_slug
from apps.lists.models import List

User = get_user_model()


class Task(TimeStampedUUIDModel):
    class TaskPriorityChoices(models.TextChoices):
        High = "High", _("High Priority")
        Middle = "Middle", _("Middle Priority")
        Low = "Low", _("Low Priority")

    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="tasks"
    )
    list = models.ForeignKey(
        List, verbose_name=_("List"), on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = models.SlugField(unique=True)
    body = models.TextField(verbose_name=_("Post"), blank=True)
    done = models.BooleanField(default=False, verbose_name=_("Done"))
    priority = models.TextField(
        choices=TaskPriorityChoices.choices, verbose_name=_("Priority")
    )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self, slugify(self.title))
        super().save(*args, **kwargs)
