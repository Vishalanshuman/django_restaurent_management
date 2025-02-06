import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    url = reverse("register")
    data = {"username": "testuser", "email": "test@example.com", "password": "password"}
    
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_order(create_user, create_food_item):
    user = create_user("john", "john@example.com", "password")
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("order-list")
    food = create_food_item()
    data = {"items": [food.id]}

    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["customer"] == user.id


@pytest.mark.django_db
def test_customer_cannot_update_order_status(create_order):
    order = create_order()
    client = APIClient()
    client.force_authenticate(user=order.customer)

    url = reverse("order-detail", kwargs={"pk": order.id})
    data = {"status": "Completed"}

    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
