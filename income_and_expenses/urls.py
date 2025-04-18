from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='income_and_expenses.index'),
]