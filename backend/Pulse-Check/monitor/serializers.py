from rest_framework import serializers
from .models import Monitor


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = [
            "id",
            "timeout",
            "alert_email",
            "status",
            "last_heartbeat",
            "task_id",
            "created_at",
        ]
        read_only_fields = ["status", "last_heartbeat", "task_id", "created_at"]