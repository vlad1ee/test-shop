from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from products.models import Category, Product, Cart


User = get_user_model()


class RecursiveCategorySerializer(serializers.HyperlinkedModelSerializer):
    children = RecursiveField(many=True)
    # products = serializers.SerializerMethodField()
    #
    # def get_products(self, obj):
    #     request = self.context.get('request')
    #     products = Product.objects.filter(category=obj)
    #     serializer = ProductSerializer(products, many=True, context={
    #         'request': request})
    #     return serializer.data

    class Meta:
        model = Category
        fields = ('title', 'url', 'parent', 'children')


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    children = RecursiveCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('url', 'title', 'parent', 'children')


class CategoryDetailSerializer(RecursiveCategorySerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        request = self.context.get('request')
        products = Product.objects.filter(category=obj)
        serializer = ProductSerializer(products, many=True, context={
            'request': request})
        return serializer.data

    class Meta:
        model = Category
        fields = ('title', 'parent', 'children', 'products')


class SizeSerializer(serializers.Serializer):
    size = serializers.CharField(max_length=255)


class ColorSerializer(serializers.Serializer):
    color = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    category = serializers.CharField(source='category.title')
    sizes = SizeSerializer(many=True)
    colors = ColorSerializer(many=True)


class CartSerializer(serializers.Serializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)
    created_at = serializers.DateTimeField()


class AddToCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id']
