from django import forms


# Форма добавления товара в корзину
class CartAddProductForm(forms.Form):
    count_item = forms.IntegerField(widget=forms.HiddenInput())
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
