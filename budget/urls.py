from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='budget.index'),
    path('delete/<int:budget_id>/', views.delete_budget, name='budget.delete'),
]