from rest_framework import generics, viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, FoodItem, Order
from .serializers import UserSerializer, FoodSerializer, OrderSerializer
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly, IsAdmin
from .services import send_order_update_emails, get_recommendations
from django.shortcuts import get_object_or_404

User = get_user_model()

class FoodViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdmin]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'name']
    ordering = ['price']

    def get_queryset(self):
        queryset = FoodItem.objects.all()
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    @swagger_auto_schema(operation_description="Retrieve a list of food items with pagination and filtering", responses={200: FoodSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new food item", request_body=FoodSerializer, responses={201: FoodSerializer})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(operation_description="Retrieve a list of orders for the authenticated user (or all orders for admin)", responses={200: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new order", request_body=OrderSerializer, responses={201: OrderSerializer})
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    @swagger_auto_schema(operation_description="Update an existing order", request_body=OrderSerializer, responses={200: OrderSerializer, 403: 'Forbidden'})
    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if request.user != order.customer:
            previous_status = order.status  

            response = super().update(request, *args, **kwargs)  

            order.refresh_from_db()  
            if order.status != previous_status:  
                send_order_update_emails(order.customer.id, order.status)

            return response

        return Response({"error": "You are not allowed to update orders."}, status=status.HTTP_403_FORBIDDEN)


class RecommendationsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Get personalized food recommendations for the user", responses={200: FoodSerializer(many=True)})
    def get(self, request):
        recommendations = get_recommendations(request.user)
        serializer = FoodSerializer(recommendations, many=True)
        return Response(serializer.data)
