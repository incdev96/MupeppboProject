import os
from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mupeppbo_project.settings")
app = Celery("mupeppbo_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-token-every-hour': {
        'task': 'send_sms_app.tasks.get_token',
        'schedule': crontab(minute='*/59'),
    }
}