import stripe
from decouple import config
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import serializers

from .utils import Google, register_social_user


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        allow_blank=True, allow_null=True, required=False
    )
    last_name = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    password = serializers.CharField()

    def save(self, **kwargs):
        (
            first_name,
            last_name,
            email,
            phone,
            address,
            password,
        ) = self.validated_data.values()
        
        try:
            password_validation.validate_password(password)

            user = get_user_model().objects._create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                password=password,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                detail={
                    "message": "User with provided credentials already exists",
                    "status": False,
                }
            )
        except ValidationError as e:
            raise serializers.ValidationError(detail=e.messages)

        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if not attrs["password1"] == attrs["password2"]:
            raise serializers.ValidationError(
                detail={
                    "message": "The two password fields didn’t match.",
                    "status": False,
                }
            )

        user = self.context["user"]

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"message": "Invalid old password"})

        return super().validate(attrs)


class PasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if not attrs["password1"] == attrs["password2"]:
            raise serializers.ValidationError(
                detail={
                    "message": "The two password fields didn’t match.",
                    "status": False,
                }
            )

        return super().validate(attrs)


class GoogleSocialAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, data):
        id_token = data.get("id_token")
        user_data = Google.validate(id_token)

        try:
            user_data["sub"]
        except Exception as identifier:
            raise serializers.ValidationError(
                {"message": str(identifier), "status": False}
            )

        # Compare the google client_id returned
        if user_data["aud"] != config("GOOGLE_CLIENT_ID"):
            raise serializers.ValidationError(
                {"message": "Invalid credentials", "status": False}
            )

        first_name, last_name, email = (
            user_data["given_name"],
            user_data["family_name"],
            user_data["email"],
        )

        return register_social_user(email, first_name, last_name)
