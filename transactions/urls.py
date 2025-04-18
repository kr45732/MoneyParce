from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='transactions.index'),
    path('/add_transaction', views.add_transaction, name='transactions.add_transaction'),
]