from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='title')
    preview = models.ImageField(upload_to='previews/', blank=True, null=True, verbose_name='preview')
    description = models.TextField(max_length=555, verbose_name='description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='title')
    description = models.TextField(max_length=555, verbose_name='description')
    preview = models.ImageField(upload_to='previews/', blank=True, null=True, verbose_name='preview')
    link = models.URLField(verbose_name='link')
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('Lesson')
        verbose_name_plural = ('Lessons')



class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'course')
