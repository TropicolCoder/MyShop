import json
from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse

# Create your views here.
from . import settings
from pypaystack import Transaction, Customer, Plan
from orders.models import Order


def process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    public_key = settings.PAYSTACK_PUBLIC_KEY
    return render(request, 'paystack/payment.html',
                  {'email': order.email, 'public_key': public_key,
                   'total_cost': total_cost})


def verify(request, id):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    transaction = Transaction(authorization_key=settings.PAYSTACK_SECRET_KEY)
    response = transaction.verify(id)
    data = JsonResponse(response, safe=False)
    verify_json = json.dumps(response)
    if verify_json[1] == '4':
        return render(request, 'paystack/failed-page.html')
    else:
        order.paid = True
        order.transaction_reference_id = id
        order.save()
        return render(request, 'paystack/success-page.html', {'order': order})


def transaction_failed(request):
    return render(request, 'paystack/failed-page.html')
