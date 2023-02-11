from django.contrib import admin
from .models import Item


# Register your models here.
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
