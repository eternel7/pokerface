from django.contrib import admin
from .models import Room, Data

admin.site.register(
    Room,
    list_display=["id", "label", "description", "portrait", "image", "staff_only", "created_at", "updated_at"],
    list_display_links=["id", "label"],
)
admin.site.register(
    Data,
    list_display=["id", "label", "description", "raw_data", "created_at", "updated_at"],
    list_display_links=["id", "label"],
)
