from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlayerViewSet, UserRegistrationAPIView, UserLoginAPIView,
    UserProfileUpdateAPIView, FriendRequestAPIView,
    UserStatsAPIView, UpdateOnlineStatusAPIView, ListFriendsAPIView,
    Enable2FAAPIView, VerifyOTPAPIView, TestEmailView, MyMatchHistoryAPIView,
    MyMatchAPIView, OAuth2LoginAPIView, OAuth2CallbackAPIView, Disable2FAAPIView,
    VerifyLoginOTPAPIView
)


router = DefaultRouter() #for standard API URL management allowing CRUD
router.register(r'players', PlayerViewSet) #registering viewsets with the router.


urlpatterns = [
    path('', include(router.urls)),
	path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('verify-login-otp/', VerifyLoginOTPAPIView.as_view(), name='verify-login-otp'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
    path('add-friend/', FriendRequestAPIView.as_view(), name='add-friend'),
    path('my-games/', MyMatchAPIView.as_view(), name='my-games'),
    path('my-matches-history/', MyMatchHistoryAPIView.as_view(), name='my-match-history'),
    path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('update-online-status/', UpdateOnlineStatusAPIView.as_view(), name='update-online-status'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('enable-2fa/', Enable2FAAPIView.as_view(), name='enable-2fa'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),  # TEST debug
    path('disable-2fa/', Disable2FAAPIView.as_view(), name='disable-2fa'),
    path('oauth/login/', OAuth2LoginAPIView.as_view(), name='oauth2_login'),
    path('oauth/callback/', OAuth2CallbackAPIView.as_view(), name='oauth2_callback'),
]
