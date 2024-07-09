from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course, Subscription


@shared_task
def send_mail_course_updated(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        send_mail(
            'Your Course Updated!',
            f'The course {course.title} has been updated.',
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.user.email],
            fail_silently=False,
        )