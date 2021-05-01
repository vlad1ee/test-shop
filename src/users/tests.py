from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserTestCase(APITestCase):

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
