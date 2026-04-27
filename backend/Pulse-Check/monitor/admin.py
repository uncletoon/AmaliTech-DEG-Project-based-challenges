from django.contrib import admin
from .models import Monitor, HeartbeatLog

admin.site.register(Monitor)
admin.site.register(HeartbeatLog)
