from django.db import models


class Monitor(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("paused", "Paused"),
        ("down", "Down"),
    )

    id = models.CharField(max_length=100, primary_key=True)
    timeout = models.PositiveIntegerField()
    alert_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Device ID: {self.id}, STATUS: {self.status}"