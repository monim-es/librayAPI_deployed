from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsAdminUserOrReadOnly  # new permission


class UserViewSet(viewsets.ModelViewSet):
    """
    Admins: full CRUD
    Members: read-only
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Everyone can read profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


class RegisterView(generics.CreateAPIView):
    """
    Open endpoint to register a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
