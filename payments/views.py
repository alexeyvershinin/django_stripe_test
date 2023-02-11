from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from payments.models import Item
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
# список объектов, главная страница
def items_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
        'title': 'home'
    }
    return render(request, 'payments/index.html', context)


# подробная информация об объекте
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {
        'item': item,
        'title': item.name,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PYBLIC_KEY
    }
    return render(request, 'payments/item_detail.html', context)


# сессия платежа
def create_session(request, item_id):
    domain = 'http://' + request.META['HTTP_HOST']
    item = Item.objects.get(id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': item.price,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                },
                'quantity': 1,
            },
        ],
        mode="payment",
        success_url=domain + '/checkout/success' + '/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=domain + '/checkout/cancel' + '/?session_id={CHECKOUT_SESSION_ID}',
    )
    return JsonResponse({'session_id': session.id})


# платеж прошел
def success_view(request):
    context = {'title': 'success'}
    return render(request, 'payments/success.html', context)


# отмена платежа
def cancel_view(request):
    context = {'title': 'cancel'}
    return render(request, 'payments/cancel.html', context)
