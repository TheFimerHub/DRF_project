from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from materials.models import Lesson, Course
from materials.serializers import LessonSerializer

User = get_user_model()

class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', description='Test Description')
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description', link="https://www.youtube.com/watch?v=test", course=self.course)

        self.lesson_list_url = reverse('materials:lesson-list')
        self.lesson_retrieve_url = reverse('materials:lesson-retrieve', args=[self.lesson.id])
        self.lesson_create_url = reverse('materials:lesson-create')
        self.lesson_delete_url = reverse('materials:lesson-delete', args=[self.lesson.id])
        self.lesson_update_url = reverse('materials:lesson-update', args=[self.lesson.id])

    def test_create_lesson(self):
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'link': 'https://www.youtube.com/watch?v=test',
            'course': self.course.id
        }
        response = self.client.post(self.lesson_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        response = self.client.get(self.lesson_list_url)
        lessons = Lesson.objects.all().order_by('id')
        serializer = LessonSerializer(lessons, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson(self):
        response = self.client.get(self.lesson_retrieve_url)
        serializer = LessonSerializer(self.lesson)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'link': 'https://www.youtube.com/watch?v=updated',
            'course': self.course.id
        }
        response = self.client.put(self.lesson_update_url, data, format='json')
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


from materials.models import Course, Subscription


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='text@example.com',password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', description='Test Description')
        self.subscription_url = reverse('materials:subscribe')

    def test_subscribe_to_course(self):
        data = {'course_id': self.course.id}
        response = self.client.post(self.subscription_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'course_id': self.course.id}
        response = self.client.post(self.subscription_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
