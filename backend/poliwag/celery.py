import os
from celery import Celery, signals
from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poliwag.settings")

app = Celery("poliwag")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Schedule periodic tasks
# Careful if you get the wrong task name here your task will not be scheduled!
app.conf.beat_schedule = {
    "sync-remote": {
        "task": "poliwag.apps.tasks.example",
        "schedule": crontab(minute="*/5"),
        # 'args': ()
    },
}

app.conf.timezone = "UTC"


@signals.task_retry.connect
@signals.task_failure.connect
@signals.task_revoked.connect
def on_task_failure(**kwargs):
    logger.exception(kwargs["exception"])


@signals.setup_logging.connect
def config_loggers(*args, **kwargs):
    # Celery overrides all logging behavior. lets not.
    from logging.config import dictConfig
    from poliwag import settings

    dictConfig(settings.LOGGING)
