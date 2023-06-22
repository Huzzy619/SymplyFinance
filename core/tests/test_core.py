import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker


User = get_user_model()


@pytest.mark.django_db
class TestViews:
    def test_forgot_password_view(self):
        url = reverse("forgot-password")
        print(url)
        client = APIClient()
        data = {"email": "test@example.com"}

        response = client.post("/accounts/forgot/password", data, format="json")

        # /accounts/forgot/password

        assert response.status_code == status.HTTP_200_OK
        # assert "message" in response.data

    # def test_password_reset_confirm_view(self):
    #     user = User.objects.create_user(username="testuser", email="test@example.com")
    #     uid = "VGVzdFVzZXI="
    #     token = "abcd1234"
    #     url = reverse("password-reset-confirm", args=[uid, token])
    #     client = APIClient()
    #     data = {"password1": "newpassword", "password2": "newpassword"}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "message" in response.data

    # def test_google_social_auth_view(self):
    #     url = reverse("google-social-auth")
    #     client = APIClient()
    #     data = {"id_token": "google_token"}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "status" in response.data

    # def test_password_update_view(self):
    #     url = reverse("password-update")
    #     user = baker.make(User)

    #     client = APIClient()
    #     client.force_authenticate(user=user)
    #     data = {"password1": "newpassword", "password2": "newpassword"}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "message" in response.data

    # def test_login_view(self):
    #     url = reverse("login")
    #     client = APIClient()
    #     data = {"email": "test@example.com", "password": "password"}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "status" in response.data
    #     assert "tokens" in response.data
    #     assert "user" in response.data

    # def test_refresh_view(self):
    #     url = reverse("token-refresh")
    #     client = APIClient()
    #     refresh_token = "refresh_token"
    #     data = {"refresh": refresh_token}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "access" in response.data
    #     assert "status" in response.data
