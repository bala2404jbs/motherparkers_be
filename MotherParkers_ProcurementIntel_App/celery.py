import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MotherParkers_ProcurementIntel_App.settings')

app = Celery('MotherParkers_ProcurementIntel_App')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
