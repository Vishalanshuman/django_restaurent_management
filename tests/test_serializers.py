import pytest
from restaurant.serializers import OrderSerializer,FoodSerializer,UserSerializer
from restaurant.models import Order

@pytest.mark.django_db
def test_order_serializer(create_order):
    order = create_order()
    serializer = OrderSerializer(order)

    assert serializer.data["customer"] == order.customer.id
    assert serializer.data["status"] == "Pending"
    assert len(serializer.data["items"]) == order.items.count()


        # fields = ['id', 'name', 'description', 'price', 'category', 'available', 'image']
@pytest.mark.django_db
def test_food_serializer(create_food_item):
    food = create_food_item()
    serializer = FoodSerializer(food)

    assert serializer.data["name"] == food.name
    assert serializer.data["description"] == food.description
    assert float(serializer.data["price"]) == food.price
    assert serializer.data["category"] == food.category
    assert serializer.data["available"] == True
    assert serializer.data["image"] == food.image

        # fields = ['id', 'username', 'email', 'password', 'role', 'profile_picture']
@pytest.mark.django_db
def test_food_serializer(create_user):
    user=create_user("testuser", "test@example.com", "password")
    serializer = UserSerializer(user)

    assert serializer.data["username"] == user.username
    assert serializer.data["email"] == user.email
    assert serializer.data["role"] == user.role
    assert serializer.data["profile_picture"] == user.profile_picture