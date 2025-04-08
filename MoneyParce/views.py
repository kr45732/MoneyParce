from django.shortcuts import render
from .models import Expense
from .utils import check_budget_status

def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    warning = check_budget_status(request.user)
    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'warning': warning,
    })
