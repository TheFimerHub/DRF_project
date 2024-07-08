from django.urls import include, path
from rest_framework import routers
from .views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonRetrieveApiView, LessonDestroyApiView, \
    LessonUpdateApiView, SubscriptionView

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

app_name = 'materials'

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/create', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/list', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>', LessonRetrieveApiView.as_view(), name='lesson-retrieve'),
    path('lessons/update/<int:pk>', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>', LessonDestroyApiView.as_view(), name='lesson-delete'),

    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),

]
