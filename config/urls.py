from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from django.contrib import admin

schema_view = get_schema_view(
   openapi.Info(
      title="Food Ordering API",
      default_version='v1',
      description="API documentation for the food ordering system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@foodapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
