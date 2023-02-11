from django.urls import path
from payments.views import item_detail, items_list, create_session, cancel_view, success_view, cart_info, cart_add, \
    cart_clear, cart_remove

urlpatterns = [
    path('', items_list, name='home'),  # главная страница
    path('item/<int:item_id>/', item_detail, name='detail_item'),  # подробная информация об объекте
    path('buy/<int:item_id>/', create_session, name='buy_item'),  # сессия платежа
    path('checkout/success/', success_view, name='success'),  # платеж прошел
    path('checkout/cancel/', cancel_view, name='cancel'),  # отмена платежа
    path('cart/', cart_info, name='list_cart'),  # корзина
    path('add/<int:item_id>', cart_add, name='add_cart'),  # добавление объекта в корзину
    path('remove/<int:item_id>', cart_remove, name='remove_cart'),  # удаление объекта из корзины
    path('clear/', cart_clear, name='clear_cart'),  # очистка корзины
    #
    # path('ordering/', create_order, name='ordering'),  # оформление заказа
]
