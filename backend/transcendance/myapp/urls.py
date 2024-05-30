from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlayerViewSet, MatchViewSet, UserRegistrationAPIView, UserLoginAPIView, 
    UserProfileUpdateAPIView, FriendRequestAPIView, MatchHistoryAPIView, 
    UserStatsAPIView, UpdateOnlineStatusAPIView, ListFriendsAPIView, 
    Enable2FAAPIView, VerifyOTPAPIView, TestEmailView, MyMatchHistoryAPIView,
    MyMatchViewSet, OAuth2LoginAPIView, OAuth2CallbackAPIView, Disable2FAAPIView,
    VerifyLoginOTPAPIView
)

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'games', MatchViewSet)
router.register(r'my-games', MyMatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('verify-login-otp/', VerifyLoginOTPAPIView.as_view(), name='verify-login-otp'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
    path('add-friend/', FriendRequestAPIView.as_view(), name='add-friend'),
    path('match-history/', MatchHistoryAPIView.as_view(), name='match-history'),
    path('my-matches-history/', MyMatchHistoryAPIView.as_view(), name='my-match-history'),
    path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('update-online-status/', UpdateOnlineStatusAPIView.as_view(), name='update-online-status'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('enable-2fa/', Enable2FAAPIView.as_view(), name='enable-2fa'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),
    path('disable-2fa/', Disable2FAAPIView.as_view(), name='disable-2fa'),
    path('oauth/login/', OAuth2LoginAPIView.as_view(), name='oauth2_login'),
    path('oauth/callback/', OAuth2CallbackAPIView.as_view(), name='oauth2_callback'),
]
