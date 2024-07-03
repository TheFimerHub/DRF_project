from rest_framework import viewsets, filters
from users.models import Payment
from users.serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paid_course__title__icontains', 'paid_lesson__title__icontains', 'payment_method']
    ordering_fields = ['payment_date']
