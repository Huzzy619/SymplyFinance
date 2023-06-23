import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_user():
    """
    Manually setting the password so that the password passes
    through all the standard hashing processes
    Only some test functions requires this (e.g Login).

    So any test that needs the user's  password to be manually set should explicitly
    add the save =True kwargs when calling get user

    This will help speed up test, instead of calling the save method 
    for all the tests functions.

    """

    def save_user(save=False):
        user = baker.make(User)
        if save:
            user.set_password("simple-password")
            user.save()

        return user

    return save_user


# @pytest.fixture
# def authenticate(api_client):
#     def authenticate_user(is_agent=False):
#         user = baker.make(User, is_agent=is_agent)
#         return api_client.force_authenticate(user=user)

#     return authenticate_user
