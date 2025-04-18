from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import ExpenseForm, IncomeForm
from .models import Expense, Income
from .utils import check_budget_status

def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    warning = check_budget_status(request.user)
    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'warning': warning,
    })
