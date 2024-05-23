from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, MatchViewSet, UserRegistrationAPIView, UserLoginAPIView, UserProfileUpdateAPIView, FriendRequestAPIView, MatchHistoryAPIView, UserStatsAPIView, UpdateOnlineStatusAPIView, ListFriendsAPIView, Enable2FAAPIView, VerifyOTPAPIView, OAuth2LoginAPIView, OAuth2CallbackAPIView
from .admin import reset_otp_secret

router = DefaultRouter() #for standard API URL management allowing CRUD
router.register(r'players', PlayerViewSet) #registering viewsets with the router.
router.register(r'games', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('update-profile/', UserProfileUpdateAPIView.as_view(), name='update-profile'),
    path('add-friend/', FriendRequestAPIView.as_view(), name='add-friend'),
    path('match-history/', MatchHistoryAPIView.as_view(), name='match-history'),
    path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
    path('update-online-status/', UpdateOnlineStatusAPIView.as_view(), name='update-online-status'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('admin/reset_otp/<str:username>/', reset_otp_secret, name='manage_otp'),
    path('enable-2fa/', Enable2FAAPIView.as_view(), name='enable-2fa'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),

		path('oauth/login/', OAuth2LoginAPIView.as_view(), name='oauth2_login'),
    path('oauth/callback/', OAuth2CallbackAPIView.as_view(), name='oauth2_callback'),
]
