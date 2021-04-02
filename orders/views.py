import os
import json
from paystack.api import signals
from paystack import utils
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import RedirectView, TemplateView
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
from . import settings
from paystack.utils import load_lib
from .forms import OrderCreateForm
from paystack.api.signals import payment_verified
from django.dispatch import receiver


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            public_key = settings.PAYSTACK_SECRET_KEY
            total_price = cart.get_total_price()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('paystack:process'))
        else:
            return HttpResponse('Invalid input try again!!!')

    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
