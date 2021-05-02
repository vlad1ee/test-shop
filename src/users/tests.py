import pdb

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self):
        user = User(username='testuser')
        password = 'testpassword1'
        user.set_password(password)
        user.save()

    def test_user_registration(self):
        url = '/api/v1/register/'
        data = {
            "username": "testuser1",
            "password": "testpass1",
            "password2": "testpass1",
            "email": "test1@mail.ru",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Token.objects.all().count(), 1)