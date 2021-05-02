from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserCreateSerializer, UserConfirmationSerializer, UserLoginSerializer

User = get_user_model()


class UserCreateAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'notification': 'На вашу почту был выслан код '
                                         'подтверждения'},
                        status=status.HTTP_201_CREATED)


class UserConfirmationAPIView(APIView):

    def post(self, request):
        data = request.data
        serializer = UserConfirmationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        verification_code = serializer.validated_data['verification_code']
        user = User.objects.filter(verification_code=verification_code)
        if user:
            user = user[0]
            user.is_active = True
            user.verification_code = None
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError('Неверный код')


class UserLoginAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token, new = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class UserLogoutAPIView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
