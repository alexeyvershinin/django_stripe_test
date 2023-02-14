from django.urls import path
from payments.views import item_detail, items_list, create_session, cancel_view, success_view, cart_info, cart_add, \
    cart_clear, cart_remove, buy_item_api, item_detail_api, success_view_api, cancel_view_api

urlpatterns = [
    path('', items_list, name='home'),  # главная страница
    path('item/<int:item_id>/', item_detail, name='detail_item'),  # подробная информация об объекте
    path('create_session/', create_session, name='checkout'),  # сессия платежа
    path('checkout/success/', success_view, name='success'),  # платеж прошел
    path('checkout/cancel/', cancel_view, name='cancel'),  # отмена платежа
    path('cart/', cart_info, name='list_cart'),  # корзина
    path('add/<int:item_id>', cart_add, name='add_cart'),  # добавление объекта в корзину
    path('remove/<int:item_id>', cart_remove, name='remove_cart'),  # удаление объекта из корзины
    path('clear/', cart_clear, name='clear_cart'),  # очистка корзины

    path('api/v1/buy/<int:item_id>/', buy_item_api, name='buy_item_api'),
    path('api/v1/item/<int:item_id>/', item_detail_api, name='item_detail_api'),
    path('api/v1/checkout/success/', success_view_api, name='success_api'),
    path('api/v1/checkout/cancel/', cancel_view_api, name='cancel_api')

]
