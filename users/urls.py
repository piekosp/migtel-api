from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserDetail, UserListCreate

app_name = "users"

urlpatterns = [
    path("", UserListCreate.as_view()),
    path("<int:pk>/", UserDetail.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
