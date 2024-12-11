import threading

import redbeat
from celery.beat import PersistentScheduler
from celery.schedules import crontab
from redbeat.schedulers import RedBeatConfig

import main
from tasks.database import periodic_backup
from utils.get_nested_value import get_nested_value
from celery import beat
from redbeat import RedBeatSchedulerEntry, RedBeatScheduler


#
# def check_and_update_cron(data):
#     """
#     Checks if the crontab exists and updates the crontab value if needed.
#     :return:
#     """
#     cron_value = get_nested_value(data, 'data', 'backup', 'cron')
#     crontab_schedule = crontab(minute="*", hour="*", day_of_week="*", day_of_month="*", month_of_year="*")
#
#     task_name = 'periodic.backup'
#     task = periodic_backup
#     task_exist = check_periodic_task(task_name)
#     if not task_exist:
#         create_periodic_task(task_name, task, crontab_schedule)
#
#
# def check_periodic_task(task_name):
#     task = main.app.tasks.get(task_name)
#     if task:
#         print(f"Task '{task_name}' exists")
#         scheduler = beat.Scheduler(app=main.app)
#         schedule = scheduler.get_schedule().get(task_name)
#         if schedule:
#             print(f"Cron schedule: {schedule.schedule}")
#         else:
#             print(f"No schedule found for task '{task_name}'")
#
#         return True
#     else:
#         print(f"Task '{task_name}' does not exist")
#         return False
#
#
# def create_periodic_task(task_name, task, crontab_schedule):
#     try:
#         main.app.add_periodic_task(
#             crontab_schedule,
#             task,
#             name=task_name
#         )
#         main.app.autodiscover_tasks()
#         print(f"Periodic task '{task_name}' created successfully")
#     except Exception as e:
#         print(f"Error creating periodic task '{task_name}': {e}")


def check_and_update_cron(data):
    cron_value = get_nested_value(data, 'data', 'backup', 'cron')
    crontab_schedule = crontab(minute="*", hour="*", day_of_week="*", day_of_month="*", month_of_year="*")
    task_name = 'periodic.backup'
    task = "tasks.database.periodic_backup"

    schedule = get_schedules()
    print(schedule)
    if f"redbeat:{task_name}" in schedule:
        print(f"Task '{task_name}' exists")
        new_cron = crontab(minute="*", hour="*", day_of_week="*", day_of_month="*", month_of_year="*/2")
        update_periodic_task(task_name, task, new_cron)
    else:
        add_task(task_name, task, crontab_schedule)
        print(f"Periodic task '{task_name}' created successfully")



def add_task(name, task, schedule):
    entry = RedBeatSchedulerEntry(name, task, schedule, args=None, kwargs=None, app=main.app)
    entry.save()


def update_periodic_task(task_name, task, crontab_schedule):
    try:
        add_task(task_name, task, crontab_schedule)
        print(f"Periodic task '{task_name}' updated successfully")
    except Exception as e:
        print(e)


#
# def create_periodic_task(task_name, task, crontab_schedule):
#     try:
#         main.app.add_periodic_task(
#             crontab_schedule,
#             task,
#             name=task_name
#         )
#         print(f"Periodic task '{task_name}' created successfully")
#     except Exception as e:
#         print(f"Error creating periodic task '{task_name}': {e}")
#
#
# def start_scheduler():
#     service = beat.Service(app=main.app)
#     service.start()

def get_schedules() -> dict:
    config = RedBeatConfig(main.app)
    schedule_key = config.schedule_key
    redis = redbeat.schedulers.get_redis(main.app)
    elements = redis.zrange(schedule_key, 0, -1, withscores=False)
    entries = {el: RedBeatSchedulerEntry.from_key(key=el, app=main.app) for el in elements}
    return entries

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
