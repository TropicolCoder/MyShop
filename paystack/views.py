import json
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView

# Create your views here.
from . import settings
from paystack.api import signals
from paystack import utils
from paystack.api.signals import payment_verified
from paystack.utils import load_lib
from .forms import CustomerInfoForm
from pypaystack import Transaction, Customer, Plan
from cart.cart import Cart
from orders.models import Order


def process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    public_key = settings.PAYSTACK_PUBLIC_KEY
    return render(request, 'paystack/payment.html',
                  {'email': order.email, 'public_key': public_key, 'total_cost': total_cost})


def verify(request, id):
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    return data
