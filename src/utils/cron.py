import logging

import redbeat
from celery.schedules import crontab
from redbeat.schedulers import RedBeatConfig
import main
from utils.get_nested_value import get_nested_value
from redbeat import RedBeatSchedulerEntry

logger = logging.getLogger('agent_logger')

def check_and_update_cron(data):
    cron_value = get_nested_value(data, 'data', 'backup', 'cron')
    if cron_value is None:
        return False

    crontab_parts = cron_value.split() if cron_value else ["*", "*", "*", "*", "*"]
    crontab_schedule = get_crontab_object(crontab_parts)
    task_name = 'periodic.backup'
    format_task_name = f"redbeat:{task_name}"
    task = "tasks.database.periodic_backup"

    schedule = get_schedules()
    logger.info(f'crontab schedule: {schedule}')

    if format_task_name in schedule:
        logger.info(f"Task '{task_name}' exists")
        actual_cron = get_crontab_as_array(schedule[format_task_name])
        if not compare_cron_arrays(actual_cron, crontab_parts):
            new_cron = get_crontab_object(crontab_parts)
            update_periodic_task(task_name, task, new_cron)

    else:
        add_task(task_name, task, crontab_schedule)
        logger.info(f"Periodic task '{task_name}' created successfully")


def add_task(name, task, schedule):
    entry = RedBeatSchedulerEntry(name, task, schedule, args=None, kwargs=None, app=main.app)
    entry.save()


def update_periodic_task(task_name, task, crontab_schedule):
    try:
        add_task(task_name, task, crontab_schedule)
        logger.info(f"Periodic task '{task_name}' updated successfully")
    except Exception as e:
        print(e)
        logger.info(e)

def get_schedules() -> dict:
    config = RedBeatConfig(main.app)
    schedule_key = config.schedule_key
    redis = redbeat.schedulers.get_redis(main.app)
    elements = redis.zrange(schedule_key, 0, -1, withscores=False)
    entries = {el: RedBeatSchedulerEntry.from_key(key=el, app=main.app) for el in elements}
    return entries

def get_crontab_as_array(entry):
    crontab_schedule = entry.schedule  # Access the schedule
    return [
        crontab_schedule._orig_minute,
        crontab_schedule._orig_hour,
        crontab_schedule._orig_day_of_month,
        crontab_schedule._orig_month_of_year,
        crontab_schedule._orig_day_of_week,
    ]

def get_crontab_object(array_entry):
    return crontab(minute=array_entry[0], hour=array_entry[1], day_of_week=array_entry[2], day_of_month=array_entry[3], month_of_year=array_entry[4])


def compare_cron_arrays(cron1, cron2):
    return cron1 == cron2


#do not delete
# @app.task(bind=True)
# def remove_periodic_tasks(self, task_names: list[str]):
#     redbeat_scheduler = RedBeatScheduler(app=app)
#
#     key_prefix = get_redbeat_key_prefix()
#
#     for task in task_names:
#         key = f"{key_prefix}:{task}"
#         entry = redbeat_scheduler.Entry.from_key(key=key, app=app)
#         entry.delete()
#
#     log_schedule_execution(self)
# Function to format crontab into an array
