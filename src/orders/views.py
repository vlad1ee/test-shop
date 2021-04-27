from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Delivery, Order
from orders.serializers import OrderSerializer, DeliverySerializer, \
    MyOrderSerializer
from products.models import Cart
from products.serializers import CartSerializer


class OrderAPIView(APIView):

    def get(self, request):
        cart_obj = Cart.objects.get_or_new(request)[0]
        cart_serializer = CartSerializer(cart_obj)
        delivery = Delivery.objects.all()
        serializer = DeliverySerializer(delivery, many=True)
        return Response({'delivery': serializer.data,
                         'cart': cart_serializer.data})

    def post(self, request):
        context = {'request': request}
        serializer = OrderSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class MyOrderAPIView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
