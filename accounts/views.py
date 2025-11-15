from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone

from .serializers import (
    RegisterSerializer, UserSerializer,
    PasswordResetRequestSerializer, SetNewPasswordSerializer
)
from .tokens import account_activation_token
from .tasks import send_email_background
from .models import AdminInvite
from .custom_permission import is_admin

User = get_user_model()


# ----------------- REGISTER -----------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # send activation email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        scheme = 'https' if self.request.is_secure() else 'http'
        link = f"{scheme}://{self.request.get_host()}/api/accounts/activate/{uid}/{token}/"
        subject = "Activate your account"
        message = f"Click to activate:\n{link}"
        send_email_background.delay(subject, message, user.email)


# ----------------- ACTIVATE -----------------
class ActivateAccountView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Account activated successfully'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


# ----------------- LOGIN -----------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'Account not active'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })


# ----------------- LOGOUT -----------------
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            print("Refresh token received for logout:", refresh_token)
            token = RefreshToken(refresh_token)
            print("Blacklisting token:", token)
            token.blacklist()
            print
            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


# ----------------- PASSWORD RESET REQUEST -----------------
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'If that account exists, an email has been sent.'}, status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        scheme = 'https' if request.is_secure() else 'http'
        link = f"{scheme}://{request.get_host()}/api/accounts/password-reset-confirm/{uid}/{token}/"

        subject = "Password Reset"
        message = f"Reset your password:\n{link}"
        send_email_background.delay(subject, message, user.email)

        return Response({'detail': 'If that account exists, an email has been sent.'}, status=status.HTTP_200_OK)


# ----------------- PASSWORD RESET CONFIRM -----------------
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data={
            'uid': uidb64,
            'token': token,
            'new_password': request.data.get('new_password')
        })
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)


# ----------------- ADMIN INVITE -----------------
class InviteAdminView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        # if not is_admin(user):
        #     return Response({'detail': 'Only admins can invite'}, status=status.HTTP_403_FORBIDDEN)

        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)

        existing = AdminInvite.objects.filter(email=email, used=False, expires_at__gt=timezone.now()).first()
        if existing:
            return Response({'detail': 'Active invite exists'}, status=status.HTTP_400_BAD_REQUEST)

        invite = AdminInvite.objects.create(email=email, invited_by=user)
        scheme = 'https' if request.is_secure() else 'http'
        link = f"{scheme}://{request.get_host()}/api/accounts/admin-register/{invite.token}/"
        subject = "Admin Invitation"
        message = f"Click to register as admin:\n{link}"
        send_email_background.delay(subject, message, email)

        return Response({'detail': 'Invitation sent'}, status=status.HTTP_200_OK)


# ----------------- ADMIN REGISTER -----------------
class AdminRegisterTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, token):
        try:
            invite = AdminInvite.objects.get(token=token)
        except AdminInvite.DoesNotExist:
            return Response({'detail': 'Invalid or expired link'}, status=status.HTTP_400_BAD_REQUEST)

        if not invite.is_valid():
            return Response({'detail': 'Link expired or used'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response({'detail': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=invite.email)
        except User.DoesNotExist:
            user = User.objects.create_superuser(email=invite.email, password=password)
            user.is_active = True
            user.save()
            invite.mark_used()
            send_email_background.delay("Admin Created", f"Your admin account is active.", invite.email)
            return Response({'detail': 'Admin account created'}, status=status.HTTP_201_CREATED)

        if user.is_staff and user.is_superuser:
            return Response({'detail': 'User already admin'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        invite.mark_used()
        send_email_background.delay("Promoted to Admin", "Your account is now admin.", invite.email)
        return Response({'detail': 'User promoted to admin'}, status=status.HTTP_200_OK)
