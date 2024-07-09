from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from materials.models import Course, Lesson, Subscription
from materials.paginator import MyPagination
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_mail_course_updated


class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = MyPagination
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('id')

    def perform_update(self, serializer):
        course = serializer.save()
        send_mail_course_updated.delay(course.id)


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer

class LessonListApiView(generics.ListAPIView):
    pagination_class = MyPagination
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.all().order_by('id')

class LessonRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')

class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')

class LessonDestroyApiView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('id')

class SubscriptionView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})
