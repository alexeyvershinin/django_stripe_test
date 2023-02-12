from django.db import models
from django.urls import reverse


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(
        verbose_name='price in cents')  # цена товара в центах, т.к. платежный сервис Stripe принимает цену в центах

    # возвращает строковое представление объекта.
    def __str__(self):
        return self.name

    # настраиваем отображение приложения в админке
    class Meta:
        ordering = ['name']  # сортировка в админке

    # возвращает URL для доступа к детальной информации о товаре
    def get_absolute_url(self):
        return reverse('detail_item', kwargs={'item_id': self.pk})

    # возвращает цену товара в долларах, для удобства отображения на страницах сайта
    def get_display_price(self):
        return '{0:.2f}'.format(self.price / 100)


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    order_price = models.FloatField(null=True)
    items = models.ManyToManyField(Item,
                                   through='PositionOrder')  # связь многие ко многим через таблицу PositionOrder

    def __str__(self):
        return f'Order №{self.pk} dated {self.date_create.strftime("%b %d, %Y")}'

    class Meta:
        ordering = ['-pk']


class PositionOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count_item = models.IntegerField()
    price = models.IntegerField()
