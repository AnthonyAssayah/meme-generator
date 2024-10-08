from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemeViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'memes', MemeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
