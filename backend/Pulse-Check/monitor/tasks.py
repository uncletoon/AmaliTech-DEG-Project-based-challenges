from celery import shared_task
from django.utils import timezone
from .models import Monitor


@shared_task
def mark_monitor_down(monitor_id):
    try:
        monitor = Monitor.objects.get(id=monitor_id)

        if monitor.status == "paused":
            return

        monitor.status = "down"
        monitor.save()

        print({
            "ALERT": f"Device {monitor.id} is down!",
            "time": timezone.now().isoformat()
        })

    except Monitor.DoesNotExist:
        return