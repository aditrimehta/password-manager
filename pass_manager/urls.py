from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaultItemViewSet

router = DefaultRouter()
router.register(r'vault', VaultItemViewSet, basename='vault')

urlpatterns = [
    path('', include(router.urls)),
]
