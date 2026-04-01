from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models import F
import logging

logger = logging.getLogger("shop_logger")
User = get_user_model()


class UserService:

    @staticmethod
    def register_user(username, password):
        user = User.objects.create_user(username=username, password=password)
        return user

    @staticmethod
    @transaction.atomic
    def top_up_balance(user, amount):
        user = User.objects.select_for_update().get(id=user.id)
        user.balance = F("balance") + amount
        user.save(update_fields=["balance"])
        user.refresh_from_db()
        logger.info(
            f"Пользователь '{user.username}' пополнил баланс на {amount}. Текущий баланс: {user.balance}"
        )
        return user.balance
