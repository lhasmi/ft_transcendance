# Unit tests for online/offline status and WebSocket, run with 'python manage.py test myapp' (09.05.2024 lhasmi)
# tests.py

import datetime
from django.utils import timezone
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator
from transcendance.asgi import application
from .models import Player, Match
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from django.db.models import Case, When, Value, BooleanField

class UserRegistrationAPITestCase(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'display_name': 'TestUser'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')


class UserLoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.get(user=self.user)

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# class FriendRequestAPITestCase(APITestCase):
#     def setUp(self):
#         self.user1 = User.objects.create_user(username='user1', password='password1')
#         self.user2 = User.objects.create_user(username='user2', password='password2')
#         self.token1 = Token.objects.get(user=self.user1)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

#     def test_add_friend(self):
#         url = reverse('add-friend')
#         data = {'username': 'user2'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Friend added successfully')
#         self.assertIn(Player.objects.get(user=self.user2), Player.objects.get(user=self.user1).friends.all())


# class UserStatsAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='player1', password='password1')
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.player = Player.objects.get(user=self.user)

#     def test_user_stats(self):
#         match1 = Match.objects.create(winner=self.player)
#         match1.players.add(self.player)
#         match2 = Match.objects.create()
#         match2.players.add(self.player)

#         url = reverse('user-stats')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['wins'], 1)
#         self.assertEqual(response.data['losses'], 1)


# class UpdateOnlineStatusAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         player = request.user.player
#         status_value = request.data.get('status')
        
#         if status_value == 'online':
#             player.online_status = True
#             message = 'Player is now online.'
#         elif status_value == 'offline':
#             player.online_status = False
#             message = 'Player is now offline.'
#         else:
#             return Response({'error': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)

#         player.save()
#         return Response({'message': message}, status=status.HTTP_200_OK)


# class WebSocketStatusConsumerTest(APITestCase):
#     async def test_websocket_status(self):
#         communicator = WebsocketCommunicator(application, "/ws/status/")
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)

#         await communicator.send_json_to({
#             'username': 'user1',
#             'online_status': True
#         })
#         response = await communicator.receive_json_from()
#         self.assertEqual(response, {
#             'username': 'user1',
#             'online_status': True
#         })
#         await communicator.disconnect()

# class PlayerStatsAPITestCase(APITestCase):
#     def setUp(self):
#         self.user1 = User.objects.create_user(username='player1', password='password1')
#         self.user2 = User.objects.create_user(username='player2', password='password2')
#         self.token1 = Token.objects.get(user=self.user1)
#         self.token2 = Token.objects.get(user=self.user2)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
#         self.player1 = Player.objects.get(user=self.user1)
#         self.player2 = Player.objects.get(user=self.user2)

#     def test_player_stats_and_match_history(self):
#         # Create a match where player1 is the winner
#         match1 = Match.objects.create()
#         match1.played_on = timezone.now() - datetime.timedelta(minutes=5)
#         match1.players.add(self.player1, self.player2)
#         match1.winner = self.player1
#         match1.save()

#         # Create another match where player2 is the winner
#         match2 = Match.objects.create()
#         match2.played_on = timezone.now()
#         match2.players.add(self.player1, self.player2)
#         match2.winner = self.player2
#         match2.save()
#         print("Match1 ID:", match1.id, "Winner ID:", match1.winner.id)
#         print("Match2 ID:", match2.id, "Winner ID:", match2.winner.id)
#         # Check individual stats for player1
#         url_stats = reverse('user-stats')
#         response_stats_player1 = self.client.get(url_stats, HTTP_ACCEPT='application/json')
#         self.assertEqual(response_stats_player1.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_stats_player1.data['wins'], 1)
#         self.assertEqual(response_stats_player1.data['losses'], 1)

#         # Check game history for player1
#         url_history = reverse('match-history')
#         response_history = self.client.get(url_history)
#         self.assertEqual(response_history.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response_history.data) >= 2)
#         print("Response status code:", response_history.status_code) #debug
#         print("Response data:", response_history.data)  # debug
#         print("Type of response data:", type(response_history.data))  # debug
#         self.assertIn('winner', response_history.data[0])  # Check structure
#         self.assertIn('players', response_history.data[0])
#         self.assertEqual(response_history.data[0]['winner']['id'], self.player2.id)
#         self.assertEqual(response_history.data[1]['winner']['id'], self.player1.id)

#         # Switch to player2 for stats
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
#         response_stats_player2 = self.client.get(url_stats, HTTP_ACCEPT='application/json')
#         self.assertEqual(response_stats_player2.status_code, status.HTTP_200_OK)
#         self.assertEqual(response_stats_player2.data['wins'], 1)
#         self.assertEqual(response_stats_player2.data['losses'], 1)

#         # Check game history for player2
#         url_history = reverse('match-history')
#         response_history_ply2 = self.client.get(url_history)
#         self.assertEqual(response_history_ply2.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response_history_ply2.data) >= 2)
#         self.assertIn('winner', response_history_ply2.data[0])  # Check structure
#         self.assertIn('players', response_history_ply2.data[0])
#         self.assertEqual(response_history_ply2.data[0]['winner']['id'], self.player2.id)
#         self.assertEqual(response_history_ply2.data[1]['winner']['id'], self.player1.id)

#         # Fetch match data after creation
#         matches = Match.objects.all().order_by('-id')  # Assuming you want the latest match first
#         for match in matches:
#             print("Match ID:", match.id, "Winner ID:", match.winner.id)
#         # Ensure the correct order of the matches
#         url_history_ordered = reverse('match-history') + '?ordering=-played_on'
#         response_history_ordered = self.client.get(url_history_ordered)
#         self.assertEqual(response_history_ordered.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response_history_ordered.data) >= 2)

#         # Validate that the order is correct (most recent first)
#         self.assertEqual(response_history_ordered.data[0]['id'], match2.id, "The first match should be the most recent")
#         self.assertEqual(response_history_ordered.data[1]['id'], match1.id, "The second match should be the older one")
        
#         # Check the details of the first and second matches in the response
#         self.assertEqual(response_history_ordered.data[0]['winner']['id'], self.player2.id)
#         self.assertEqual(response_history_ordered.data[1]['winner']['id'], self.player1.id)

#         # Output additional debug information if needed
#         print("Ordered History Response:", response_history_ordered.data)



# class MatchHistoryAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='player1', password='password1')
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.player = Player.objects.get(user=self.user)

#     def test_match_history(self):
#         match = Match.objects.create()
#         match.players.add(self.player)
#         url = reverse('match-history')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response.data) > 0)
# class WebSocketGameConsumerTest(APITestCase):
#     async def test_websocket_game(self):
#         communicator = WebsocketCommunicator(application, "/ws/game/chess_room/")
#         connected, _ = await communicator.connect()
#         self.assertTrue(connected)

#         await communicator.send_json_to({
#             'move': 'e2e4'
#         })

#         response = await communicator.receive_json_from()
#         self.assertEqual(response, {
#             'move': 'e2e4'
#         })

#         await communicator.disconnect()



# Unit tests for endpoints, run with 'python manage.py test myapp' (06.05.2024 lhasmi)

# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from .models import Player, Match


# class UserRegistrationAPITestCase(APITestCase):
#     def test_user_registration(self):
#         url = reverse('register')
#         data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'testuser@example.com',
#             'display_name': 'TestUser'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['message'], 'User created successfully')


# class UserLoginAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.token = Token.objects.get(user=self.user)

#     def test_user_login(self):
#         url = reverse('login')
#         data = {
#             'username': 'testuser',
#             'password': 'testpassword'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class FriendRequestAPITestCase(APITestCase):
#     def setUp(self):
#         self.user1 = User.objects.create_user(username='user1', password='password1')
#         self.user2 = User.objects.create_user(username='user2', password='password2')
#         self.token1 = Token.objects.get(user=self.user1)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

#     def test_add_friend(self):
#         url = reverse('add-friend')
#         data = {'username': 'user2'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Friend added successfully')
#         self.assertIn(Player.objects.get(user=self.user2), Player.objects.get(user=self.user1).friends.all())


# class MatchHistoryAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='player1', password='password1')
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.player = Player.objects.get(user=self.user)

#     def test_match_history(self):
#         match = Match.objects.create()
#         match.players.add(self.player)
#         url = reverse('match-history')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response.data) > 0)


# class UserStatsAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='player1', password='password1')
#         self.token = Token.objects.get(user=self.user)
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         self.player = Player.objects.get(user=self.user)

#     def test_user_stats(self):
#         match1 = Match.objects.create(winner=self.player)
#         match1.players.add(self.player)
#         match2 = Match.objects.create()
#         match2.players.add(self.player)

#         url = reverse('user-stats')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['wins'], 1)
#         self.assertEqual(response.data['losses'], 1)

