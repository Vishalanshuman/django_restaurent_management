import pytest
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import CustomUser, FoodItem, Order
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()

@pytest.fixture
def create_user(db):
    def make_user(username, email, password, role="customer"):
        return User.objects.create_user(username=username, email=email, password=password, role=role)
    return make_user

@pytest.fixture
def create_food_item(db):
    def make_food(name="Burger", price=10.99, category="Fast Food", available=True):
        return FoodItem.objects.create(name=name, price=price, category=category, available=available)
    
    return make_food  

@pytest.fixture
def create_order(db, create_user, create_food_item):
    def make_order(user=None, items=None, status="Pending"):
        if user is None:
            user = create_user("testuser", "test@example.com", "password")
        if items is None:
            items = [create_food_item()]

        total_price = sum(item.price for item in items)
        order = Order.objects.create(customer=user, status=status, total_price=total_price)
        order.items.set(items)
        return order

    return make_order


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(create_user):
    return create_user("admin", "admin@example.com", "password", role="admin")

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user("testuser", "test@example.com", "password")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client, user

@pytest.fixture
def admin_authenticated_client(api_client, admin_user):
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    print(api_client.credentials.headers)
    return api_client, admin_user
