from django.contrib.auth.models import User
from django.shortcuts import render, redirect

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