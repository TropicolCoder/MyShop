from django.urls import path
from django.urls import re_path as url
from django.views.decorators.csrf import csrf_exempt
from . import views


app_name = 'orders'


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]
