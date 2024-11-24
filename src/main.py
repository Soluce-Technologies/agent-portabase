from celery import Celery
from kombu import Exchange, Queue
from settings import config
from celery.schedules import crontab
from tasks.tasks import ping_server

app = Celery('my_celery_app')
app.conf.broker_url = config.CELERY_BROKER_URL
app.conf.result_backend = config.CELERY_RESULT_BACKEND
app.conf.broker_connection_retry_on_startup = True

# Registering an exchange and two queues
default_exchange = Exchange('default', type='topic')

app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default.#'),
    Queue('periodic', default_exchange, routing_key='periodic.#'),
)

# Configuring default queue, exchange and routing key
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'

app.autodiscover_tasks()

# Configuring tasks routes
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
