from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import OrderService
from .serializers import OrderSerializer


class CheckoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            order = OrderService.create_order_from_cart(request.user)
            serializer = OrderSerializer(order)
            return Response(
                {
                    "message": "Заказ успешно оформлен и оплачен!",
                    "order": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
