from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import CartItemAddSerializer, CartItemDetailSerializer
from .services import CartService


class CartAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemAddSerializer

    def get(self, request):
        cart = CartService.get_or_create_cart(request.user)
        items = cart.items.select_related("product").all()
        serializer = CartItemDetailSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            CartService.add_product_to_cart(
                user=request.user,
                product_id=serializer.validated_data["product_id"],
                quantity=serializer.validated_data["quantity"],
            )
            return Response(
                {"message": "Товар добавлен в корзину"}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
