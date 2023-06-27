import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.management.utils import get_random_secret_key as random_password
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import  urlsafe_base64_encode
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create register test first_name,
            


@pytest.mark.django_db
class TestRegister:
    url = reverse("register")
    data = {
            "first_name":"test_first", 
            "last_name":"test_last",
            "email": "user@example.com",
            "phone": "+2349066757334",
            "address": "This is my address",
            "password": "simple-password"
         }
    
    def test_successful_registration_return_200(self, api_client):
         
         
         response = api_client.post(self.url, self.data)

         assert response.status_code == status.HTTP_201_CREATED
    
    def test_user_already_exists_return_400(self, api_client, get_user):

        user = get_user(save = True)

        data  = self.data.update({"email":user.email})
        
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_invalid_password_return_400(self, api_client):
        
        data  = self.data.update({"password": "1234"})
        response = api_client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        


          

@pytest.mark.django_db
class TestForgotPassword:
    def test_valid_email_returns_200(self, api_client, get_user):
        url = reverse("forgot-password")

        data = {"email": get_user().email}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_email_returns_404(self, api_client, get_user):
        url = reverse("forgot-password")

        data = {"email": "jargons" + get_user().email}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPasswordResetConfirm:
    bad_uid = "MjI1OTMwZTQtNzFlYy00NTU0LTgwM2ItZTg4NzU1MmNiZjA4"
    bad_token = "bq8314-c1d590c5d513f620a77224d2bd60e754"

    def test_password_reset_confirm_return_200(self, api_client, get_user):
        user = get_user()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse("password-reset-confirm", args=[uid, token])
        password = random_password()
        data = {"password1": password, "password2": password}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_token_return_400(self, api_client, get_user):
        # Correct uid but invalid_tokens
        uid = urlsafe_base64_encode(force_bytes(get_user().pk))

        url = reverse("password-reset-confirm", args=[uid, self.bad_token])
        password = random_password()
        data = {"password1": password, "password2": password}

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_no_user_found_return_404(self, api_client):
        url = reverse("password-reset-confirm", args=[self.bad_uid, self.bad_token])

        password = random_password()
        data = {"password1": password, "password2": password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["status"] is False

    def test_if_password_does_not_pass_validation_returns_403(
        self, api_client, get_user
    ):
        user = get_user()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse("password-reset-confirm", args=[uid, token])

        # Put a cheeky password that would fail validation
        password = "1234"

        data = {"password1": password, "password2": password}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPasswordUpdate:
    def test_password_update_return_200(self, api_client, get_user):
        url = reverse("password-update")

        user = get_user(save=True)

        get_user()

        api_client.force_authenticate(user=user)

        data = {
            "old_password": "simple-password",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_old_password_return_400(self, api_client, get_user):
        url = reverse("password-update")

        api_client.force_authenticate(user=get_user())

        data = {
            "old_password": "wrong password",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert True is True


@pytest.mark.django_db
class TestLogin:
    def test_successful_login_return_200(self, api_client, get_user):
        url = reverse("login")

        user = get_user(save=True)
        data = {"email": user.email, "password": "simple-password"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "status" in response.data
        assert "tokens" in response.data
        assert "user" in response.data

    def test_invalid_login_return_401(self, api_client, get_user):
        url = reverse("login")

        user = get_user(save=True)
        data = {"email": user.email, "password": "wrong-password"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["status"] is False

    def test_refresh_token_return_200(self, api_client, get_user):
        url = reverse("token-refresh")
        refresh_token = "refresh_token"

        refresh_token = RefreshToken.for_user(get_user())
        data = {"refresh": str(refresh_token)}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    # def test_google_social_auth_view(self):
    #     url = reverse("google-social-auth")
    #     client = APIClient()
    #     data = {"id_token": "google_token"}

    #     response = client.post(url, data, format="json")

    #     assert response.status_code == status.HTTP_200_OK
    #     assert "status" in response.data
