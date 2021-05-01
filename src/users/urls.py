from django.urls import path, include

from users.views import UserCreateAPIView, UserConfirmationAPIView

urlpatterns = [
    path('auth/', include('djoser.urls'), name='auth'),
    path('auth/', include('djoser.urls.jwt'), name='auth'),
    path('register/', UserCreateAPIView.as_view()),
    path('confirm/', UserConfirmationAPIView.as_view())
]
