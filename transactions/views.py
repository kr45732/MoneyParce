from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from MoneyParce.forms import ExpenseForm, IncomeForm
from MoneyParce.models import Expense, Income


# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Transactions'

    expense_form = ExpenseForm()
    income_form = IncomeForm()

    # .filter(user=request.user) preferred over .all()
    expenses = Expense.objects.all()
    incomes = Income.objects.all()

    return render(request, 'transactions/index.html', {
        'expense_form': expense_form,
        'income_form': income_form,
        'expenses': expenses,
        'incomes': incomes,
        'template_data': template_data
    })


def add_transaction(request):

    # Test user, DELETE ONCE LOGIN IS IMPLEMENTED!!
    if not request.user.is_authenticated:
        user, created = User.objects.get_or_create(username='exampleuser')
        request.user = user

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

def remove_transaction(request, transaction_id, transaction_type):
    if not request.user.is_authenticated:
        user, created = User.objects.get_or_create(username='exampleuser')
        request.user = user
        # redirect user in production
        # return redirect("login")

    if transaction_type == 'expense':
        transaction = get_object_or_404(Expense, id=transaction_id, user=request.user)
    elif transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id, user=request.user)
    else:
        raise Http404("Transaction type not found.")

    transaction.delete()
    return redirect("transactions.index")