from rest_framework import viewsets, permissions
from .models import VaultItem
from .serializers import VaultItemSerializer
from django.http import HttpResponse   

def home(request):
    return HttpResponse("Welcome to the Password Manager")

class VaultItemViewSet(viewsets.ModelViewSet):
    serializer_class = VaultItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VaultItem.objects.filter(user=self.request.user)


