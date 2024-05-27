from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlayerViewSet, MatchViewSet, UserRegistrationAPIView, UserLoginAPIView, 
    UserProfileUpdateAPIView, FriendRequestAPIView, MatchHistoryAPIView, 
    UserStatsAPIView, UpdateOnlineStatusAPIView, ListFriendsAPIView, 
    Enable2FAAPIView, VerifyOTPAPIView, TestEmailView, MyMatchHistoryAPIView,
    MyMatchViewSet, OAuth2LoginAPIView, OAuth2CallbackAPIView
)

router = DefaultRouter() #for standard API URL management allowing CRUD
router.register(r'players', PlayerViewSet) #registering viewsets with the router.
router.register(r'games', MatchViewSet)
router.register(r'my-games', MyMatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
    path('add-friend/', FriendRequestAPIView.as_view(), name='add-friend'),
    path('match-history/', MatchHistoryAPIView.as_view(), name='match-history'),
    path('my-matches-history/', MyMatchHistoryAPIView.as_view(), name='my-match-history'),
    path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('update-online-status/', UpdateOnlineStatusAPIView.as_view(), name='update-online-status'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    # bellow path MUST stay: is used to enable 2FA for a user by generating a secret key and sending an OTP via email. 
    # It allows the user to activate 2FA on their account.
    path('enable-2fa/', Enable2FAAPIView.as_view(), name='enable-2fa'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),  # TEST debug
    
    path('oauth/login/', OAuth2LoginAPIView.as_view(), name='oauth2_login'),
    path('oauth/callback/', OAuth2CallbackAPIView.as_view(), name='oauth2_callback'),
]
