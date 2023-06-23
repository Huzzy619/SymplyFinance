
from decouple import config
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.signals import user_logged_in

from .serializers import (
    ForgotPasswordSerializer,
    GoogleSocialAuthSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordUpdateSerializer,
    RegisterSerializer,
)

class Testing(GenericAPIView):

    def get(self, request):

        from django.urls import reverse
        
        print(reverse("forgot-password"))

        return Response("ok")
    
class RegisterView(GenericAPIView):
    """
    Create an account

    Returns:

        new_user: A newly registered user
    """

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Registered successfully",
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = get_user_model().objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = config("FRONTEND_URL", request.get_host())
            token = default_token_generator.make_token(user)

            print(uid, token)
            link = f"{request.scheme}://{domain}/account/reset/password/confirm/{uid}/{token}"

            send_mail(
                subject="RESET PASSWORD",
                message=f"click this link to proceed to reset password  \n{link}",
                recipient_list=[user.email],
                from_email="admin@studebt.com",
            )
            return Response(
                {"message": "email containing link to reset password has been sent"}, 
                status=status.HTTP_200_OK
            )
        except get_user_model().DoesNotExist:
            pass
            # When No user is found, just ignore
        return Response(          
            {"message": "User not found.", "status": False},
            status=status.HTTP_404_NOT_FOUND
            )


class PasswordResetConfirm(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is None:
            return Response(
                {"message": "User not found.", "status": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"message": "Invalid, expired or already used token.", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password1"]

        if not user.is_superuser: #! To free admin users from password validation
            try:
                password_validation.validate_password(password, user)
            except ValidationError as e:
                return Response(
                    {"message": e, "status": False}, status=status.HTTP_403_FORBIDDEN
                )

        user.set_password(password)
        user.save()

        return Response(
            {"message": "success", "detail": "password changed successfully"}, 
            status=status.HTTP_200_OK
        )

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            ValidationError,
            get_user_model().DoesNotExist,
        ):
            user = None
        return user


class GoogleSocialAuthView(GenericAPIView):
    """
    Login with Google by providing Auth_token

    Args:
        Auth_token
    """

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"
        Send an id token from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["status"]: True
        return Response(data, status=status.HTTP_200_OK)


class PasswordUpdateView(GenericAPIView):
    """
    Change password

    """

    permission_classes = [IsAuthenticated]
    serializer_class = PasswordUpdateSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data["password1"]

        try:
            password_validation.validate_password(password, request.user)
        except Exception as e:
            return Response(
                {"message": e, "status": False}, status=status.HTTP_403_FORBIDDEN
            )

        request.user.set_password(password)
        request.user.save()
        return Response(
            {"message": "Password updated successfully", "status": True},
            status=status.HTTP_200_OK,
        )


class LoginView(GenericAPIView):
    """
    Login with Email & Password to get Authentication tokens

    Args:

        Login credentials (_type_):  email && password

    Returns:

        message: success

        tokens: access and refresh

        user: user profile details
    """

    serializer_class = LoginSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email, password = serializer.validated_data.values()
        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                {"message": "Email or password is incorrect", "status": False},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # if not user.is_verified:
        #     return Response(
        #             {"message": "You must verify your email first", "status": False},
        #             status=status.HTTP_401_UNAUTHORIZED,
        #     )

        refresh = RefreshToken.for_user(user)

        user_logged_in.send_robust(get_user_model(), user=user)

        return Response(
            {
                "status": True,
                "message": "Logged in successfully",
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                "user": {
                    "id": user.pk,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class RefreshView(TokenRefreshView):
    """
    To get new access token after the initial one expires or becomes invalid

    Args:
        refresh_token

    Returns:
        access_token
    """

    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            access_token = serializer.validated_data["access"]
            return Response(
                {"access": access_token, "status": True}, status=status.HTTP_200_OK
            )
        except TokenError:
            return Response({"error": "Token is invalid or expired"}, status=401)
        