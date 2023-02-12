from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from payments.forms import CartAddProductForm
from payments.models import Item, Order, PositionOrder
from payments.cart import Cart
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
        # 'STRIPE_PUBLIC_KEY': settings.STRIPE_PYBLIC_KEY,
        'form': CartAddProductForm()
    }
    return render(request, 'payments/item_detail.html', context)


# сессия платежа
def create_session(request):
    domain = 'http://' + request.META['HTTP_HOST']
    cart = Cart(request)

    # Создаем заказ и записываем в него выбранные позиции корзины
    order = Order.objects.create(order_price=cart.get_total_full_price())
    for item in cart:
        PositionOrder.objects.create(
            order=order,
            item=item['item'],
            price=int(item['price_item']) * int(item['count_item']),
            count_item=item['count_item'],
        )

    # Создаем строку с названиями и ценами товаров
    items = '\n'.join(
        f"- {item['item'].name}: {item['count_item']} pieces for {int(item['price_item']) / 100:.2f} USD" for item in
        cart)

    # Создаем объект Checkout Session, который будет обрабатывать платеж
    session_args = {
        'payment_method_types': ['card'],
        'line_items': [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(order.order_price) * 100),  # Цена в центах
                    'product_data': {
                        'name': order,
                        'description': items,
                    },
                },
                'quantity': 1,
            },
        ],
        'mode': "payment",
        'success_url': domain + '/checkout/success' + '/?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url': domain + '/checkout/cancel' + '/?session_id={CHECKOUT_SESSION_ID}'
    }

    # Забираем скидку из созданного заказа
    discount = order.order_discount.discount_percentage

    # Если скидка больше 0, то создаем купон и добавляем его в Checkout Session
    if discount > 0:
        coupon = stripe.Coupon.create(percent_off=discount, duration="once")
        session_args['discounts'] = [{'coupon': coupon.id}]

    session = stripe.checkout.Session.create(**session_args)

    # Возвращаем ID Checkout Session в JSON-формате
    return JsonResponse({'session_id': session.id})


# платеж прошел
def success_view(request):
    Cart(request).clear()
    messages.success(request, 'The payment was successful!')
    return render(request, 'payments/messages.html', {'title': 'success'})


# отмена платежа
def cancel_view(request):
    messages.error(request, 'Payment cancelled!')
    return render(request, 'payments/messages.html', {'title': 'cancel'})


# добавление объекта в корзину
@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item_obj = get_object_or_404(Item, pk=item_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cart.add(
            item=item_obj,
            count_item=form.cleaned_data['count_item'],
            update_count=form.cleaned_data['update']
        )

    return redirect('list_cart')


# удаление объекта из корзины
def cart_remove(request, item_id):
    cart = Cart(request)
    item_obj = get_object_or_404(Item, pk=item_id)
    cart.remove(item=item_obj)
    messages.success(request, 'The item was successfully removed from the shopping cart')
    return redirect('list_cart')


# Корзина покупателя
def cart_info(request):
    cart = Cart(request)
    context = {
        'cart': cart,
        'title': 'shopping cart',
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PYBLIC_KEY
    }
    return render(request, 'cart/cart.html', context)


# очистка корзины
def cart_clear(request):
    Cart(request).clear()
    messages.success(request, 'Cart has been successfully cleared')
    return redirect('home')
