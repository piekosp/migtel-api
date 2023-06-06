from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    EmployeeSetupView,
    PasswordReset,
    PasswordResetRequest,
    UserDetailView,
    UserEmailVerificationView,
    UserListCreateView,
    UserSelfDetailView,
)

app_name = "users"

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user_list_create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("me/", UserSelfDetailView.as_view(), name="user_self_detail"),
    path(
        "activate/<int:pk>/<str:token>/",
        UserEmailVerificationView.as_view(),
        name="user_active",
    ),
    path(
        "employee_setup/<int:pk>/<str:token>/",
        EmployeeSetupView.as_view(),
        name="employee_setup",
    ),
    path(
        "password_reset/", PasswordResetRequest.as_view(), name="password_reset_request"
    ),
    path(
        "password_reset/<int:pk>/<str:token>/",
        PasswordReset.as_view(),
        name="password_reset",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
