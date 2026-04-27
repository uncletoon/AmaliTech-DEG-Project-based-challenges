from celery.result import AsyncResult
from django.utils import timezone

from monitor.models import Monitor
from monitor.tasks import mark_monitor_down


def schedule_timer(monitor):
    task = mark_monitor_down.apply_async( # type: ignore
        args=[monitor.id],
        countdown=monitor.timeout
    )

    monitor.task_id = task.id
    monitor.save(update_fields=["task_id"])


def cancel_timer(monitor):
    if monitor.task_id:
        AsyncResult(monitor.task_id).revoke()
        monitor.task_id = None
        monitor.save(update_fields=["task_id"])


def create_monitor(validated_data):
    monitor = Monitor.objects.create(
        id=validated_data["id"],
        timeout=validated_data["timeout"],
        alert_email=validated_data["alert_email"],
        status="active",
        last_heartbeat=timezone.now(),
    )

    schedule_timer(monitor)
    return monitor


def handle_heartbeat(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)

    cancel_timer(monitor)

    monitor.status = "active"
    monitor.last_heartbeat = timezone.now()
    monitor.save(update_fields=["status", "last_heartbeat"])

    schedule_timer(monitor)
    return monitor


def pause_monitor(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)

    cancel_timer(monitor)

    monitor.status = "paused"
    monitor.save(update_fields=["status"])

    return monitor