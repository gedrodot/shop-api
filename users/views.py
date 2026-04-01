from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    BalanceTopUpSerializer,
)
from .services import UserService
import logging

logger = logging.getLogger("shop_logger")


class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.register_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        return Response(
            UserProfileSerializer(user).data, status=status.HTTP_201_CREATED
        )


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class BalanceTopUpView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BalanceTopUpSerializer

    def post(self, request):
        serializer = BalanceTopUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_balance = UserService.top_up_balance(
            user=request.user, amount=serializer.validated_data["amount"]
        )
        return Response(
            {
                "message": f"Баланс успешно пополнен на {serializer.validated_data['amount']}",
                "new_balance": new_balance,
            },
            status=status.HTTP_200_OK,
        )
