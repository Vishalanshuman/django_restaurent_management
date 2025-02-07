from . models import FoodItem,Order
from django.db.models import Count
from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()



def get_recommendations(user):
    previous_orders = Order.objects.filter(customer=user)
    ordered_items = FoodItem.objects.filter(order__in=previous_orders).distinct()

    popular_items = FoodItem.objects.annotate(order_count=Count('order')).order_by('-order_count')[:5]

    preferred_items = FoodItem.objects.filter(
        category__in=[item.category for item in ordered_items]
    ).exclude(id__in=ordered_items)
    recommendations = list(ordered_items) + list(popular_items) + list(preferred_items)

    return list(set(recommendations))

def send_order_update_emails(user_id,status):
    try:

        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"You Order Update"
        message = f"Your Order status is changed : {status} at {today}"
        user= User.objects.filter(id=user_id).first()

        recipients = [user.email] 

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
        print("Email Sent ---->")
    except Exception as e:
        print("Error sending email:",e.__str__())