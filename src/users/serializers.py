import random
import string

from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from rest_framework import serializers


User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError('Пользователь с таким логином '
                                              'уже существует')
        else:
            return value

    def validate_password(self, value):
        if self.initial_data['password2'] == value:
            return value
        else:
            raise serializers.ValidationError('Пароли не совпадают')


    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        sequence = string.ascii_letters + string.digits
        verification_code = ''.join(random.sample(sequence, 15))
        user = User(**validated_data, is_active=False,
                    verification_code=verification_code)
        user.set_password(password)
        user.save()
        subject = 'Подтверждение аккаунта'
        message = f'{verification_code}'
        from_email = 'online.shop.sunrise@gmail.com'
        to_email = [validated_data.get('email')]
        send_mail(subject, message, from_email, to_email)
        return user


class UserConfirmationSerializer(serializers.Serializer):
    verification_code = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, values):
        user = authenticate(**values)
        if user:
            values['user'] = user
            return values
        else:
            raise serializers.ValidationError('Неверные данные')
