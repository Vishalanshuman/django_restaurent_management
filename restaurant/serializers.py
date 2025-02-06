from rest_framework import serializers
from .models import CustomUser,FoodItem,Order
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'profile_picture']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'category', 'available', 'image']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all(), many=True)
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'total_price', 'status']
        read_only_fields = ['id','customer', 'total_price']

    def create(self, validated_data):
        items = validated_data['items']
        total_price = sum(item.price for item in items)

        
        validated_data['total_price'] = total_price
        validated_data['status'] = 'Pending'
        
        return super().create(validated_data)
