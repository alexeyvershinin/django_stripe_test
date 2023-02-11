from django.conf import settings
from .models import Item


# корзина покупателя
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        # Обновление ключа "cart" в сессии
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметка сессии в опции "измененный", для обновления и сохранения данных
        self.session.modified = True

    def add(self, item, count_item=1, update_count=False):
        item_pk = str(item.pk)

        # Проверка наличия продукта в корзине (если нет в корзине, то добавляем)
        if item_pk not in self.cart:
            self.cart[item_pk] = {
                'count_item': 0,
                'price_item': str(item.price)
            }

        # Обновление количества объектов в корзине
        if update_count:
            self.cart[item_pk]['count_item'] = count_item
        else:
            self.cart[item_pk]['count_item'] += count_item

        # Сохранение корзины в сессию
        self.save()

    def remove(self, item):
        item_pk = str(item.pk)

        # Если удаляемый товар лежит в корзине, то очищаем его ключ (и данные о нём)
        if item_pk in self.cart:
            del self.cart[item_pk]

            self.save()

    def get_total_full_price(self):
        return '{0:.2f}'.format(
            sum(int(item['price_item']) * int(item['count_item']) / 100 for item in self.cart.values()))

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(int(item['count_item']) for item in self.cart.values())

    def __iter__(self):
        # Получение первичных ключей
        list_item_pk = self.cart.keys()

        # Загрузка данных из БД
        list_item_obj = Item.objects.filter(pk__in=list_item_pk)

        # Копирование корзины для дальнейшей работы
        cart = self.cart.copy()
        # Перебор и добавление объектов(записей) из БД
        for item_obj in list_item_obj:
            cart[str(item_obj.pk)]['item'] = item_obj

        for item in cart.values():
            item['total_price'] = '{0:.2f}'.format((int(item['price_item']) * int(item['count_item']) / 100))

            yield item
