from django.shortcuts import render

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

def transactions(request):
    # .filter(user=request.user) preferred over .all()
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    expense_form = ExpenseForm()
    income_form = IncomeForm()

    return render(request, 'transactions.html', {
        'expense_form': expense_form,
        'income_form': income_form,
        'expenses': expenses,
        'incomes': incomes,
    })

def add_transaction(request):
    expense_form = ExpenseForm()
    income_form = IncomeForm()

    if request.method == 'POST':
        if 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()
        elif 'add_income' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                income.save()

    # Fetch updated transactions
    # .filter(user=request.user) preferred over .all()

    expenses = Expense.objects.all()
    incomes = Income.objects.all()

    return render(request, 'transactions.html', {
        'expense_form': expense_form,
        'income_form': income_form,
        'expenses': expenses,
        'incomes': incomes,
    })