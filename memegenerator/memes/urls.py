from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemeViewSet, MemeTemplateViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'memes', MemeViewSet)
router.register(r'templates', MemeTemplateViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
