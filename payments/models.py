from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(verbose_name='price in cents')  # центы, т.к. stripe API принимает цену в центах

    def __str__(self):
        return self.name
