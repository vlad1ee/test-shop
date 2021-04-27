from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Category, Product, Cart
from products.serializers import CategorySerializer, CategoryDetailSerializer, \
    ProductSerializer, CartSerializer, AddToCartSerializer


class CategoryAPIView(APIView):

    def get(self, request):
        serializer_context = {'request': request}
        categories = Category.objects.prefetch_related('products').filter(
            parent=None)
        serializer = CategorySerializer(categories, many=True,
                                        context=serializer_context)
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        serializer_context = {'request': request}
        category = Category.objects.prefetch_related('products').get(pk=pk)
        serializer = CategoryDetailSerializer(category,
                                              context=serializer_context)
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request):
        serializer_context = {'request': request}
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True,
                                       context=serializer_context)
        return Response(serializer.data)


class CartAddAPIView(APIView):
    def get(self, request):
        cart_obj, new_obj = Cart.objects.get_or_new(request)
        serializer = CartSerializer(cart_obj)
        return Response(serializer.data)

    def post(self, request):
        cart = Cart.objects.get_or_new(request)[0]
        serializer_context = {'request': request}
        serializer = AddToCartSerializer(data=request.data,
                                         context=serializer_context)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product,
                                    pk=serializer.validated_data.get('id'))
        if product in cart.products.all():
            cart.products.remove(product)
        else:
            cart.products.add(product)
        return Response(status=status.HTTP_200_OK)
