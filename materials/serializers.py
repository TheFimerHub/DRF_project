from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.services import DashboardApiPayCourse
from materials.validators import YouTubeURLValidator
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeURLValidator(field='link')]

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    session = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_product(self, obj):
        api = DashboardApiPayCourse()
        product = api.create_product(name=obj.title, description=obj.description)
        return product

    def get_price(self, obj):
        api = DashboardApiPayCourse()

        currency='rub'
        payment = Payment.objects.filter(id=obj.id).first()
        if not payment:
            return None

        unit_amount = int(payment.amount * 100)
        product_data = self.get_product(obj)


        product = api.create_price(currency=currency, unit_amount=unit_amount, product_data=product_data)

        return product

    def get_session(self, obj):
        api = DashboardApiPayCourse()
        price_data = self.get_price(obj)
        if not price_data:
            return None

        success_url = self.context['request'].build_absolute_uri('/success/')
        cancel_url = self.context['request'].build_absolute_uri('/cancel/')

        payment = Payment.objects.filter(id=obj.id).first()
        if not payment:
            return None

        payment_method_types = 'card'

        session = api.create_session(
            success_url=success_url,
            cancel_url=cancel_url,
            price_id=price_data['id'],
            payment_method_types=payment_method_types
        )
        return session

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
