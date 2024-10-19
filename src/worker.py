import redis
from celery import Celery
from celery.schedules import crontab

from settings import config

celery = Celery(__name__)
celery.conf.broker_url = config.CELERY_BROKER_URL
celery.conf.result_backend = config.CELERY_RESULT_BACKEND


redis_client = redis.StrictRedis(host=config.REDIS_SERVER, port=config.REDIS_PORT, db=0)


@celery.task(name="ping_server")
def ping_server():
    print("Ping the server Portabase")

    return True


if config.DEBUG:
    ping_crontab = crontab(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )
else:
    ping_crontab = crontab(
        minute='*/5',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

celery.add_periodic_task(
    ping_crontab,
    ping_server,
    name="ping_server",
)
