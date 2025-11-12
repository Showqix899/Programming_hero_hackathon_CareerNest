from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    ActivateAccountView,
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    InviteAdminView,
    AdminRegisterTokenView,
)

urlpatterns = [
    # ----------------- Authentication -----------------
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ----------------- Password Reset -----------------
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # ----------------- Admin -----------------
    path('admin-invite/', InviteAdminView.as_view(), name='admin_invite'),
    path('admin-register/<token>/', AdminRegisterTokenView.as_view(), name='admin_register'),
]
