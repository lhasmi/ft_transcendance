from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, MatchViewSet, UserRegistrationAPIView, UserLoginAPIView, UserProfileUpdateAPIView, FriendRequestAPIView, MatchHistoryAPIView, UserStatsAPIView, UpdateOnlineStatusAPIView, ListFriendsAPIView
from .admin import reset_otp_secret

router = DefaultRouter() #for standard API URL management allowing CRUD
router.register(r'players', PlayerViewSet) #registering viewsets with the router.
router.register(r'games', MatchViewSet)#to be tested

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
]
# path('send-friend-request/<int:to_player_id>/', FriendRequestAPIView.as_view(), name='send-friend-request'),
# path('accept-friend-request/<int:request_id>/', AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
# path('update-online-status/', UpdateOnlineStatusAPIView.as_view(), name='update-online-status'),
# path('list-online-friends/', ListOnlineFriendsAPIView.as_view(), name='list-online-friends'),
# path('match-history/', MatchHistoryAPIView.as_view(), name='match-history'),
# path('user-stats/', UserStatsAPIView.as_view(), name='user-stats'),
