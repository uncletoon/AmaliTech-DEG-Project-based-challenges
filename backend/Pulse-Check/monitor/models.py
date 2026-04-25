from django.db import models
from django.utils import timezone

# Create your models here.
class Monitor(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('down', 'Down'),
        ('paused', 'Paused'),
    )

    id = models.CharField(max_length=100, primary_key=True)
    timeout = models.PositiveIntegerField(help_text="Timeout in seconds")
    alert_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_heartbeat = models.DateTimeField(default=timezone.now)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True, help_text="Developer's Choice: URL to notify when device goes down")

    def __str__(self):
        return f"{self.id} ({self.status})"