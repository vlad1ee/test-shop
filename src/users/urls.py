from django.urls import path, include

from users.views import UserCreateAPIView, UserConfirmationAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path('auth/', include('djoser.urls'), name='auth'),
    path('auth/', include('djoser.urls.jwt'), name='auth'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('confirm/', UserConfirmationAPIView.as_view()),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout')
]
