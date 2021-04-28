from django.contrib import admin
from django.urls import path, include
from . import yasg


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('orders.urls'))
]

urlpatterns += yasg.urlpatterns