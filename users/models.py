from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('transfer', 'Transfer to Account'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='course_payments')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='lesson_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    def __str__(self):
        return f'Payment by {self.user.email} on {self.payment_date}'

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'