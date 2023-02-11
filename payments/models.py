from django.db import models
from django.urls import reverse


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(verbose_name='price in cents')  # центы, т.к. stripe API принимает цену в центах

    def __str__(self):
        return self.name

    # настраиваем отображение приложения в админке
    class Meta:
        ordering = ['name']  # сортировка в админке

    # определяем метод, которым выстраиваем ссылку для подробного описания объекта и передаем ее в шаблон
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'item_id': self.pk})

    # данный метод вернет цену в долларах
    def get_display_price(self):
        return '{0:.2f}'.format(self.price / 100)
