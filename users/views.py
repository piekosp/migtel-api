from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import (
    CanDeleteUser,
    CanEditUser,
    CanEditUserRole,
    CanSeeUserDetails,
    IsManager,
    IsManagerOrSelf,
)
from .serializers import (
    EmployeeSetupSerializer,
    PasswordResetRequestSerializer,
    PasswordSerializer,
    UserSerializer,
)
from .tasks import (
    send_activation_email,
    send_employee_setup_email,
    send_password_reset_email,
)
from .tokens import activation_token, employee_setup_token, password_reset_token


class UserListCreateView(views.APIView):
    def get_permissions(self):
        permission_classes = []
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated, IsManager]
        return [permission() for permission in permission_classes]

    def get_queryset(self, request):
        if request.user.role == User.ADMIN:
            return User.objects.all()
        return User.employees.all()

    def send_email_with_token(self, request, user):
        if request.user.is_authenticated and request.user.role in User.MANAGER_ROLES:
            token = employee_setup_token.make_token(user)
            send_employee_setup_email(user, token)
        else:
            token = activation_token.make_token(user)
            send_activation_email(user, token)

    def get(self, request, format=None):
        queryset = self.get_queryset(request)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(context={"request": request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_email_with_token(request, user)
        return Response(serializer.data)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        IsManagerOrSelf,
        CanSeeUserDetails,
        CanDeleteUser,
        CanEditUser,
        CanEditUserRole,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserEmailVerificationView(views.APIView):
    def post(self, request, pk, token, format=None):
        user = get_object_or_404(User, pk=pk)
        if not activation_token.check_token(user, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class PasswordReset(views.APIView):
    def post(self, request, pk, token, format=None):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, pk=pk)
        if not password_reset_token.check_token(user, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        password = serializer.validated_data["password"]
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class PasswordResetRequest(views.APIView):
    def post(self, request, format=None):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)
        token = password_reset_token.make_token(user)
        send_password_reset_email(user, token)
        return Response(status=status.HTTP_200_OK)


class EmployeeSetupView(views.APIView):
    def post(self, request, pk, token, format=None):
        user = get_object_or_404(User, pk=pk)
        if not employee_setup_token.check_token(user, token):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = EmployeeSetupSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
