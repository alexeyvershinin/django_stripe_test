from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(1000)  # центы, т.к. stripe API принимает цену в центах

    def __str__(self):
        return self.name
