from django.db import models
from django.urls import reverse


# Create your models here.
# скидка
class Discount(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name="order_discount")
    discount_percentage = models.PositiveIntegerField(default=0)

    # вычисляем и сохраняем скидку на заказ
    def save(self, *args, **kwargs):
        order_total = float(self.order.order_price)
        if order_total >= 100:
            self.discount_percentage = 10
        elif order_total >= 50:
            self.discount_percentage = 5
        super().save(*args, **kwargs)

    # возвращает строковое представление объекта.
    def __str__(self):
        return f'{self.discount_percentage}% discount on {self.order}'


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


# заказ
class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    order_price = models.FloatField(null=True)
    items = models.ManyToManyField(Item,
                                   through='PositionOrder')  # связь многие ко многим через таблицу PositionOrder

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order_price:
            Discount.objects.get_or_create(order=self)

    def __str__(self):
        return f'Order №{self.pk} dated {self.date_create.strftime("%b %d, %Y")}'

    class Meta:
        ordering = ['-pk']


# позиции в заказе
class PositionOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count_item = models.IntegerField()
    price = models.IntegerField(verbose_name='price in cents')

    class Meta:
        verbose_name_plural = 'Positions in order'
