from django.urls import path
from .views import item_detail, items_list

urlpatterns = [
    path('', items_list, name='home'),  # главная страница
    path('item/<int:item_id>/', item_detail, name='item_detail')  # подробная информация об объекте
]
