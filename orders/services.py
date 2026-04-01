from django.db import transaction
from django.core.exceptions import ValidationError
from cart.models import Cart
from catalog.models import Product
from .models import Order, OrderItem
import logging
from django.db.models import F

logger = logging.getLogger("shop_logger")


class OrderService:

    @staticmethod
    def create_order_from_cart(user):
        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            raise ValidationError("Корзина пуста")

        try:
            with transaction.atomic():
                user = type(user).objects.select_for_update().get(id=user.id)

                total_amount = sum(
                    item.product.price * item.quantity for item in cart.items.all()
                )

                if user.balance < total_amount:
                    raise ValidationError("Недостаточно средств")

                product_ids = cart.items.values_list("product_id", flat=True)
                products_locked = {
                    p.id: p
                    for p in Product.objects.select_for_update().filter(
                        id__in=product_ids
                    )
                }

                order = Order.objects.create(user=user, total_amount=total_amount)

                for cart_item in cart.items.all():
                    product = products_locked[cart_item.product_id]

                    if product.stock < cart_item.quantity:
                        raise ValidationError(
                            f"Недостаточно товара, в наличии: {product.stock}"
                        )

                    product.stock = F("stock") - cart_item.quantity
                    product.save(update_fields=["stock"])

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price_at_moment=product.price,
                        quantity=cart_item.quantity,
                    )

                user.balance = F("balance") - total_amount
                user.save(update_fields=["balance"])

                cart.items.all().delete()

        except Exception as e:
            raise e

        OrderService.notify_success(order)
        return order

    @staticmethod
    def notify_success(order):
        msg = (
            f"Заказ #{order.id} от {order.user.username} на сумму {order.total_amount} "
        )
        logger.info(msg)
