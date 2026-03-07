from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "notification_type", "is_read", "push_sent", "created_at"]
    list_filter = ["notification_type", "is_read", "push_sent"]
    search_fields = ["user__email", "title"]
    raw_id_fields = ["user"]
