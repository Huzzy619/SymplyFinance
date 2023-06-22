from django.conf import settings
from django.contrib.auth import get_user_model
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework import response, status
from rest_framework_simplejwt.tokens import RefreshToken


def register_social_user(email, first_name, last_name):
    user = get_user_model().objects.filter(email=email).first()

    if not user:
        user = get_user_model().objects.create_user(
            email=email,
            password=settings.SECRET_KEY,
            first_name=first_name,
            last_name=last_name,
        )
    refresh = RefreshToken.for_user(user)

    access = refresh.access_token

    return {
        "tokens": {"access": str(access), "refresh": str(refresh)},
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name, 
            "last_name": user.last_name
        },
    }


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, google_requests.Request())

            if "accounts.google.com" in idinfo["iss"]:
                return idinfo
        except Exception:
            return response.Response(
                {
                    "message": "The token is either invalid or has expired",
                    "status": False,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
