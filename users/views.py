from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import UserCreateSerializer, UserDetailSerializer, UserListSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserListSerializer
        return UserCreateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return super().get_permissions()
        return []


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]
