from django.shortcuts import render, get_object_or_404

from payments.models import Item


# Create your views here.
# список объектов, главная страница
def items_list(request):
    items = Item.objects.all()
    context = {
        'items': items,
        'title': 'home'
    }
    return render(request, 'payments/index.html', context)


# подробная информация об объекте
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {
        'item': item,
        'title': item.name
    }
    return render(request, 'payments/item_detail.html', context)
