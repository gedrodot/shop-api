from django.db import transaction
from .models import Cart, CartItem
from catalog.models import Product
from django.core.exceptions import ValidationError


class CartService:
    @staticmethod
    def get_or_create_cart(user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    @transaction.atomic
    def add_product_to_cart(user, product_id, quantity):
        try:
            product = Product.objects.select_for_update().get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Товар не найден")

        if product.stock < quantity:
            raise ValidationError(f"Недостаточно товара, в наличии: {product.stock}")

        cart = CartService.get_or_create_cart(user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            new_quantity = cart_item.quantity + quantity
        else:
            new_quantity = quantity

        if product.stock < new_quantity:
            raise ValidationError(f"Недостаточно товара, в наличии: {product.stock}")

        cart_item.quantity = new_quantity
        cart_item.save()
        return cart_item
