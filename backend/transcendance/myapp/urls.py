from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, GameViewSet, UserRegistrationAPIView, UserLoginAPIView, UserProfileUpdateAPIView

router = DefaultRouter() #for standard API URL management allowing CRUD
router.register(r'players', PlayerViewSet) #registering viewsets with the router.
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
]
