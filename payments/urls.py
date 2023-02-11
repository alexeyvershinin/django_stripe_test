from django.urls import path
from .views import item_detail

urlpatterns = [
    path('item/<int:pk>/', item_detail),
]