import pytest
from cart.models import Cart, CartItem


@pytest.mark.django_db
class TestCartAPI:

    def test_view_empty_cart(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)

        response = api_client.get("/api/cart/")

        assert response.status_code == 200
        assert response.data == []

    def test_add_product_to_cart(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)

        payload = {"product_id": product.id, "quantity": 2}
        response = api_client.post("/api/cart/", payload)

        assert response.status_code == 201
        assert "добавлен" in response.data["message"]

        cart = Cart.objects.get(user=test_user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 2

    def test_add_existing_product_increases_quantity(
        self, api_client, test_user, product
    ):
        api_client.force_authenticate(user=test_user)

        api_client.post("/api/cart/", {"product_id": product.id, "quantity": 2})
        api_client.post("/api/cart/", {"product_id": product.id, "quantity": 3})

        cart = Cart.objects.get(user=test_user)
        items_count = CartItem.objects.filter(cart=cart).count()
        assert items_count == 1

        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 5

    def test_add_product_exceeds_stock(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)

        payload = {"product_id": product.id, "quantity": 15}
        response = api_client.post("/api/cart/", payload)

        assert response.status_code == 400
        assert "Недостаточно товара" in response.data["error"]

        assert not CartItem.objects.filter(product=product).exists()
