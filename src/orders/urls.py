from django.urls import path

from orders.views import OrderAPIView, MyOrderAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view(), name='orders'),
    path('my-orders/', MyOrderAPIView.as_view(), name='my-orders'),
]