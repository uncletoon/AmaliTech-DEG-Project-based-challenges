import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pulse_check_project.settings")

app = Celery("pulse_check_project") # type: ignore
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()