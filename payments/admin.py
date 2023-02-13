from django.contrib import admin
from .models import Item, Order, PositionOrder, Discount, Tax


# Register your models here.
# товары
class ItemAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'name', 'description', 'price')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'name')
    # поля по которым будет производиться поиск
    search_fields = ('name',)
    # поля, которые будем использовать для фильтрации
    list_filter = ('name', 'price')


# регистрируем модель и наш класс настроек
admin.site.register(Item, ItemAdmin)


# регистрируем модель Order(заказ)
admin.site.register(Order)


# позиции в заказе
class PositionOrderAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'order', 'item', 'count_item', 'price')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('order',)


# регистрируем модель и наш класс настроек
admin.site.register(PositionOrder, PositionOrderAdmin)


# Скидка
class DiscountAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'name', 'conditions')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'name')


# регистрируем модель и наш класс настроек
admin.site.register(Discount, DiscountAdmin)


# Налог
class TaxAdmin(admin.ModelAdmin):
    # список полей для отображения
    list_display = ('id', 'name', 'tax_percentage')
    # поля, которые будут являться ссылками на объект
    list_display_links = ('id', 'name')


# регистрируем модель и наш класс настроек
admin.site.register(Tax, TaxAdmin)
