import pytest


@pytest.mark.django_db
class TestCatalogAPI:

    def test_public_can_view_products(self, api_client, product):
        response = api_client.get("/api/catalog/products/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Laptop"

    def test_user_cannot_create_product(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        payload = {"name": "Hacker Phone", "price": 100, "stock": 5}
        response = api_client.post("/api/catalog/products/", payload)

        assert response.status_code == 403

    def test_admin_can_create_product(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        payload = {"name": "Admin Phone", "price": "100.00", "stock": 5}
        response = api_client.post("/api/catalog/products/", payload)

        assert response.status_code == 201
