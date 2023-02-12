from django import template
from payments.cart import Cart
from payments.models import Item

register = template.Library()


# общее количество товаров в корзине
@register.simple_tag(takes_context=True)
def cart_item_count(context):
    request = context['request']
    cart = Cart(request)
    return len(cart)


# количество уникальных наименований товаров в корзине
@register.simple_tag(takes_context=True)
def cart_obj_count(context):
    cart = context.request.session.get('cart', {})
    item_pks = list(cart.keys())
    item_count = Item.objects.filter(pk__in=item_pks).count()
    return item_count


# отображение скидки в корзине покупателя
@register.simple_tag(takes_context=True)
def show_discount(context):
    request = context['request']
    cart = Cart(request)
    discount = 0
    if float(cart.get_total_full_price()) >= 100:
        discount = 10
    elif float(cart.get_total_full_price()) >= 50:
        discount = 5
    final_price = float(cart.get_total_full_price()) - (float(cart.get_total_full_price()) * discount / 100)
    return final_price, discount
