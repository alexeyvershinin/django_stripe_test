from django.urls import path
from .views import item_detail, items_list, create_session, cancel_view, success_view

urlpatterns = [
    path('', items_list, name='home'),  # главная страница
    path('item/<int:item_id>/', item_detail, name='detail_item'),  # подробная информация об объекте
    path('buy/<int:item_id>/', create_session, name='buy_item'),  # сессия платежа
    path('checkout/success/', success_view, name='success'),  # платеж прошел
    path('checkout/cancel/', cancel_view, name='cancel')  # отмена платежа
]
