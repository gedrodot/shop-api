import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="buyer", password="password123", balance=1000
    )


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username="admin", password="admin123")


@pytest.fixture
def product():
    return Product.objects.create(name="Laptop", price=500, stock=10)
