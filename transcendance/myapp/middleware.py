from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from urllib.parse import parse_qs

from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import urllib.parse
import logging

User = get_user_model()
logger = logging.getLogger(__name__) # for debug, willp rint statements of what happens

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = dict(urllib.parse.parse_qsl(query_string))
        token = query_params.get("token")
        logger.debug(f"Query string: {query_string}")
        logger.debug(f"Token: {token}")
        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token["user_id"]
                user = await self.get_user(user_id)
                scope["user"] = user
                logger.debug(f"User authenticated: {user}")
            except Exception as e:
                scope["user"] = AnonymousUser()
                logger.debug(f"Authentication failed: {e}")
        else:
            scope["user"] = AnonymousUser()
            logger.debug("No token provided, anonymous user")

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()

# AuthMiddlewareStack now uses TokenAuthMiddleware instead of default
def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))

# @database_sync_to_async
# def get_user(token):
#     try:
#         UntypedToken(token)# Validate the token and decode it
#     except (InvalidToken, TokenError) as e:
#         return AnonymousUser()# If the token is invalid, return an anonymous user
   
#     decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"]) # Decode the token to get user information
#     user_id = decoded_data.get("user_id")
#     try:
#         return User.objects.get(id=user_id)# Get the user from the database
#     except User.DoesNotExist:
#         return AnonymousUser() # If user does not exist, return an anonymous user

# class TokenAuthMiddleware(BaseMiddleware):
#     async def __call__(self, scope, receive, send):
#         # Close old database connections to prevent usage of timed out connections
#         close_old_connections()
#         query_string = parse_qs(scope["query_string"].decode())# Extract token from query string
#         token = query_string.get("token")
#         if token:
#             scope["user"] = await get_user(token[0])# Attach user to the scope if token is valid
#         else:
#             scope["user"] = AnonymousUser()# Attach anonymous user if no token is provided
#         return await super().__call__(scope, receive, send)# Call the next middleware or application
