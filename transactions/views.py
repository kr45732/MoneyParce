from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from MoneyParce.forms import ExpenseForm, IncomeForm
from MoneyParce.models import Expense, Income


@login_required

def index(request):
    template_data = {'title': 'Transactions'}

    expense_form = ExpenseForm()
    income_form = IncomeForm()

    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    return render(request, 'transactions/index.html', {
        'expense_form': expense_form,
        'income_form': income_form,
        'expenses': expenses,
        'incomes': incomes,
        'template_data': template_data
    })

@login_required
def add_transaction(request):
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

    return redirect("transactions.index")

@login_required
def remove_transaction(request, transaction_id, transaction_type):
    if transaction_type == 'expense':
        transaction = get_object_or_404(Expense, id=transaction_id, user=request.user)
    elif transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id, user=request.user)
    else:
        raise Http404("Transaction type not found.")

    transaction.delete()
    return redirect("transactions.index")