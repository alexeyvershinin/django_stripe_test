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
