from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='transactions.index'),
    path('add_transaction', views.add_transaction, name='transactions.add_transaction'),
    path('remove_transaction/<str:transaction_type>/<int:transaction_id>/', views.remove_transaction, name='transactions.remove_transaction'),
]