from django.urls import path

from orders.views import OrderAPIView, MyOrderAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view()),
    path('my-orders/', MyOrderAPIView.as_view()),
]