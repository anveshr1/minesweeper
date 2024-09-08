from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.game import GameViewSet

router = DefaultRouter()
router.register('game', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]