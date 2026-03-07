from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import RegisterView, ProfileView, FCMTokenView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="auth-logout"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("profile/fcm-token/", FCMTokenView.as_view(), name="user-fcm-token"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
