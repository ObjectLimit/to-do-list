from django.contrib import admin

from apps.lists.models import List


class ListAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    list_filter = ["author"]


admin.site.register(List, ListAdmin)
