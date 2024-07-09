from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .services import set_schedule
        set_schedule(
            task_name='deactivate_inactive_users',
            task_function='users.tasks.deactivate_inactive_users',
            every=1,  # Каждую минуту
            period='minutes',
        )
