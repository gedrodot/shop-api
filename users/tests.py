import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUsersAPI:

    def test_registration(self, api_client):
        payload = {"username": "new_user", "password": "password123!@#"}
        response = api_client.post("/api/users/register/", payload)
        assert response.status_code == 201
        assert User.objects.filter(username="new_user").exists()

    def test_topup_balance(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)

        response = api_client.post("/api/users/topup/", {"amount": 500})

        assert response.status_code == 200
        test_user.refresh_from_db()
        assert test_user.balance == 1500
