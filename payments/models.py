from django.db import models
from django.urls import reverse


# Create your models here.
# налог
class Tax(models.Model):
    name = models.CharField(max_length=100, null=True)
    tax_percentage = models.PositiveIntegerField()  # процент налога


# скидка
class Discount(models.Model):
    name = models.CharField(max_length=100, null=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    conditions = models.PositiveIntegerField(default=0)  # условия для скидки

    def __str__(self):
        return self.name


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
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    tax = models.ManyToManyField(Tax)


    def __str__(self):
        return f'Order №{self.pk} dated {self.date_create.strftime("%b %d, %Y")}'

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # поскольку налог один, сделаем пока так, в будущем можно написать методы для присвоения различных налогов
        self.tax.set(Tax.objects.filter(name='NDS'))

        # получаем скидки, где условия ниже, чем общая стоимость заказа
        discounts = Discount.objects.filter(conditions__lte=float(self.order_price)).order_by('-discount_percentage')

        # применяем скидку к заказу
        if discounts.exists():
            discount = discounts.first()
            self.discount = discount
            self.__class__.objects.filter(pk=self.pk).update(discount=discount)


# позиции в заказе
class PositionOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count_item = models.IntegerField()
    price = models.IntegerField(verbose_name='price in cents')

    class Meta:
        verbose_name_plural = 'Positions in order'
