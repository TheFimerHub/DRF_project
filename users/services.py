# users/services.py
from celery import Celery
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

app = Celery('config')

# Отрабатывает в apps.py
def set_schedule(task_name, task_function, schedule_time, task_args=None):
    """
    Устанавливает расписание для задачи Celery.

    :param task_name: Имя задачи.
    :param task_function: Полный путь к функции задачи.
    :param schedule_time: Время расписания в формате crontab (например, {'minute': 0, 'hour': 0}).
    :param task_args: Аргументы задачи (необязательно).
    """
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute=schedule_time.get('minute', '*'),
        hour=schedule_time.get('hour', '*'),
        day_of_week=schedule_time.get('day_of_week', '*'),
        day_of_month=schedule_time.get('day_of_month', '*'),
        month_of_year=schedule_time.get('month_of_year', '*'),
    )

    PeriodicTask.objects.update_or_create(
        name=task_name,
        defaults={
            'crontab': schedule,
            'task': task_function,
            'args': json.dumps(task_args or []),
        },
    )