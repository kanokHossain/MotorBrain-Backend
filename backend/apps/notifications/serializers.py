from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "notification_type", "title", "body", "data",
            "is_read", "push_sent", "push_sent_at", "vehicle", "created_at",
        ]
        read_only_fields = ["id", "push_sent", "push_sent_at", "created_at"]
