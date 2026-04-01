from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "В обработке"),
        ("paid", "Оплачен"),
        ("shipped", "Отправлен"),
        ("cancelled", "Отменен"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="paid")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Итоговая сумма"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_at_moment = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Заказ #{self.order.id})"
