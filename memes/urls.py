from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import MemeViewSet, MemeTemplateViewSet, RatingViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'memes', MemeViewSet, basename='meme')
router.register(r'templates', MemeTemplateViewSet, basename='template')
router.register(r'ratings', RatingViewSet, basename='rating')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth-token/', obtain_auth_token),  # Token generation
]
