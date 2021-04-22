from django.urls import path

from products.views import CategoryAPIView, CategoryDetailAPIView, \
    ProductAPIView, CartAddAPIView


urlpatterns = [
    path('category/', CategoryAPIView.as_view()),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(),
         name='category-detail'),
    path('products/', ProductAPIView.as_view()),
    path('cart/', CartAddAPIView.as_view()),
]