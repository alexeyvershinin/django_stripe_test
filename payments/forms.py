from django import forms

# PROD_MAX_COUNT = [(i, str(i)) for i in range(1, 21)]


# Форма добавления товара в корзину
class CartAddProductForm(forms.Form):
    # count_item = forms.TypedChoiceField(choices=PROD_MAX_COUNT, coerce=int, label='Quantity:')
    count_item = forms.IntegerField(widget=forms.HiddenInput())
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
