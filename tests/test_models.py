import pytest
from restaurant.models import Order

@pytest.mark.django_db
def test_create_order(create_user, create_food_item):
    user = create_user("john", "john@example.com", "password")

    food = [create_food_item(name, price) for name, price in {
        "Burger": 10.99,
        "Pizza": 15.99,
        "Pasta": 8.99,
        "Salad": 5.99,
        "Sushi": 12.99,
    }.items()]

    total_price = sum(item.price for item in food)
    order = Order.objects.create(customer=user, status="Pending",total_price=total_price)
    order.items.set(food)  

    assert order.customer == user
    assert order.status == "Pending"
    assert order.items.count() == len(food)  
    assert order.total_price == sum(item.price for item in food)  
