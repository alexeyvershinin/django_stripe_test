from django import template
from payments.cart import Cart
from payments.models import Item, Discount, Tax

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
    # получаем все скидки условия которых ниже стоимости всех товаров в корзине
    discounts = Discount.objects.filter(conditions__lte=float(cart.get_total_full_price())).order_by(
        '-discount_percentage')
    if discounts.exists():
        discount = discounts.first().discount_percentage
    else:
        discount = 0

    tax = Tax.objects.get(name='NDS').tax_percentage  # процент налога, принимаем во внимание, что налог у нас один

    total_price = float(cart.get_total_full_price())  # цена товаров в корзине без скидки и налога
    discount_amount = total_price * discount / 100  # вычисляем скидку
    final_price = total_price - discount_amount  # цена с учетом скидки
    tax_amount = final_price * tax / 100  # вычисляем налог
    final_price_with_tax = final_price + tax_amount  # итоговая цена

    return final_price_with_tax, discount, tax
