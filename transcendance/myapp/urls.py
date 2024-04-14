from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, GameViewSet
from django.contrib import admin

router = DefaultRouter() #choice for straightforward API URL management
router.register(r'players', PlayerViewSet) #registering viewsets with the router.
router.register(r'games', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
	path('admin/', admin.site.urls),
]
# includs routed URLs in the application’s URL patterns.
