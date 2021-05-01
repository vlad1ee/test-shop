import pdb

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders.models import Order, Delivery
from products.models import Category, Cart, Product

User = get_user_model()


class ProductAPITestCase(APITestCase):

    def setUp(self):
        category = Category.objects.create(title='Мужская одежда')
        self.user = User.objects.create(
            username="testuser1",
            password="testpass1",
            email="test1@mail.ru"
        )
        Product.objects.create(title='Рубашка', price=2500, category=category)
        cart = Cart.objects.create(user=self.user)
        delivery = Delivery.objects.create(title='Быстрая доставка',
                                           description='weqweqweeqwe',
                                           price=200)
        Order.objects.create(cart=cart, address='Бишкек',
                             delivery=delivery)

    def test_get_products(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category(self):
        url = reverse('category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        qs = Category.objects.filter(title='Мужская одежда')
        self.assertEqual(qs.count(), 1)

    def test_category_detail(self):
        url = '/api/v1/category/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'title': 'Мужская одежда',
                                         'parent': None, 'children': [],
                                         'products': [
                                             {'title': 'Рубашка',
                                              'description': '',
                                              'price': '2500.00',
                                              'category': 'Мужская одежда',
                                              'sizes': [], 'colors': []}]})

    def test_cart(self):
        url = reverse('cart')
        data = {'id': 1}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_get(self):
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery'][0]['title'], 'Быстрая '
                                                                'доставка')
        self.assertEqual(response.data['cart']['products'], [])

    def test_order_create(self):
        url = reverse('orders')
        data = {'cart': 1, 'delivery': 1, 'address': 'Бишкек'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_my_orders(self):
        url = reverse('my-orders')
        response = self.client.get(url)
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user'), 'AnonymousUser')
