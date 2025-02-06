from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import FoodViewSet, OrderViewSet, RecommendationsView,RegisterUserView

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/recommendations/', RecommendationsView.as_view(), name='recommendations'),
]

router = DefaultRouter()
router.register(r'api/food-items', FoodViewSet, basename='food') 
router.register(r'api/orders', OrderViewSet, basename='order')  

urlpatterns += router.urls
