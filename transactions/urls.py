from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='transactions.index'),
    path('add_transaction', views.add_transaction, name='transactions.add_transaction'),
    path('remove_transaction/<str:transaction_type>/<int:transaction_id>/', views.remove_transaction, name='transactions.remove_transaction'),
    path('exchange_public_token', views.exchange_public_token, name='transactions.exchange_public_token'),
    path('create_link_token', views.create_link_token, name='transactions.create_link_token'),
    path('sync_transactions', views.sync_transactions, name='transactions.sync_transactions'),
]