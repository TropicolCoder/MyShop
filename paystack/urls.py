from django.urls import re_path as url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import settings
from . import views

urlpatterns = [
    path('process/', views.process, name='process'),
    path('verify/<str:id>', views.verify, name='verify'),
    path('failed/', views.transaction_failed, name='failed'),
]
