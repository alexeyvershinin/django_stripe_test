from django.shortcuts import render, get_object_or_404
from payments.models import Item


# Create your views here.
def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    context = {'item': item}
    return render(request, 'payments/item_detail.html', context)
