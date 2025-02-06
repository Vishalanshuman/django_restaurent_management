from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import CustomUser, FoodItem, Order
from .serializers import UserSerializer, FoodSerializer, OrderSerializer
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime,timedelta
from django.contrib.auth import get_user_model


User = get_user_model()




class FoodViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminUser]
    filter_backends = (SearchFilter, OrderingFilter)  

    search_fields = ['name', 'category']  
    ordering_fields = ['price', 'name']  
    ordering = ['price']  

    def get_queryset(self):
        queryset = FoodItem.objects.all()

        name = self.request.query_params.get('name', None)
        category = self.request.query_params.get('category', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    @swagger_auto_schema(
        operation_description="Retrieve a list of food items with pagination and filtering",
        responses={200: FoodSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new food item",
        request_body=FoodSerializer,
        responses={201: FoodSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a list of orders for the authenticated user (or all orders for admin)",
        responses={200: OrderSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderSerializer,
        responses={201: OrderSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing order",
        request_body=OrderSerializer,
        responses={200: OrderSerializer, 403: 'Forbidden'}
    )
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user == order.customer:
            return Response(
                {"error": "You are not allowed to update orders."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
def send_order_update_emails(user_id,status):

    today = datetime.now().strftime('%Y-%m-%d')
    subject = f"You Order Update"
    message = f"Your Order status is changed : {status}"
    user= User.objects.filter(id=user_id).first()

    recipients = [user.email] 

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )

class AdminOrderStatusUpdateView(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Admin update order status",
        responses={200: openapi.Response('Order status updated', OrderSerializer)}
    )
    def partial_update(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        order.status = request.data.get('status', order.status)
        order.save()
        send_order_update_emails(order.customer.id)
        return Response({'status': order.status})

def get_recommendations(user):
    previous_orders = Order.objects.filter(customer=user)
    ordered_items = FoodItem.objects.filter(order__in=previous_orders).distinct()

    popular_items = FoodItem.objects.annotate(order_count=Count('order')).order_by('-order_count')[:5]

    preferred_items = FoodItem.objects.filter(
        category__in=[item.category for item in ordered_items]
    ).exclude(id__in=ordered_items)
    recommendations = list(ordered_items) + list(popular_items) + list(preferred_items)

    return list(set(recommendations))

class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get personalized food recommendations for the user",
        responses={200: FoodSerializer(many=True)}
    )
    def get(self, request):
        recommendations = get_recommendations(request.user)
        serializer = FoodSerializer(recommendations, many=True)
        return Response(serializer.data)
