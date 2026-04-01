import pytest
from cart.models import Cart, CartItem


@pytest.mark.django_db
class TestOrderAPI:

    def test_checkout_success(self, api_client, test_user, product):
        api_client.force_authenticate(user=test_user)
        cart = Cart.objects.create(user=test_user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        response = api_client.post("/api/orders/checkout/")

        assert response.status_code == 201
        assert "Заказ успешно оформлен" in response.data["message"]

        test_user.refresh_from_db()
        product.refresh_from_db()

        assert test_user.balance == 500
        assert product.stock == 9
        assert cart.items.count() == 0
