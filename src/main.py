import logging
import os
import sys
import warnings
from logging.config import dictConfig

from celery import Celery
from celery.signals import worker_process_init
from kombu import Exchange, Queue

from logging_config import setup_logging
from settings import config
from celery.schedules import crontab
from tasks.tasks import ping_server
from utils.init import initialize_directories


def create_celery_app():
    app = Celery('portabase-agent')
    app.conf.broker_url = config.CELERY_BROKER_URL
    app.conf.result_backend = config.CELERY_RESULT_BACKEND
    app.conf.broker_connection_retry_on_startup = True

    default_exchange = Exchange('default', type='topic')

    app.conf.task_queues = (
        Queue('default', default_exchange, routing_key='default.#'),
        Queue('periodic', default_exchange, routing_key='periodic.#'),
    )

    # Configuring default queue, exchange, and routing key
    app.conf.task_default_queue = 'default'
    app.conf.task_default_exchange = 'default'
    app.conf.task_default_routing_key = 'default'

    app.autodiscover_tasks()

    CELERY_TASK_ROUTES = {
        'default.*': {
            'queue': 'default',
            'routing_key': 'default.#',
        },
        'periodic.*': {
            'queue': 'periodic',
            'routing_key': 'periodic.#',
        }
    }

    ping_crontab = crontab(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    app.add_periodic_task(
        ping_crontab,
        ping_server,
        name="periodic.ping_server",
        bind=True,
    )

    return app


def run_initialization():
    if not initialize_directories():
        sys.exit(1)

    warnings.filterwarnings("ignore", category=UserWarning)

    if os.getenv("ENVIRONMENT") != "development":
        setup_logging()

    return create_celery_app()


app = run_initialization()

