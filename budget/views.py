from django.shortcuts import render, redirect
from MoneyParce.models import Expense, Budget
from MoneyParce.utils import check_budget_status
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    template_data = {'title': 'MoneyParce - Budget', 'section': 'Budget'}

    budgets = Budget.objects.filter(user=request.user)

    # For each budget, calculate amount spent and percent used
    for budget in budgets:
        if budget.category == "ALL":
            expenses = Expense.objects.filter(user=request.user)
        else:
            expenses = Expense.objects.filter(user=request.user, category=budget.category)

        total_spent = sum(exp.amount for exp in expenses)
        if budget.limit > 0:
            budget.percent_used = round((total_spent / budget.limit) * 100, 2)
        else:
            budget.percent_used = 0

        budget.amount_spent = total_spent  # Optional: if you want to show dollars spent too

    if request.method == 'POST':
        limit = request.POST.get('limit')
        category = request.POST.get('category')

        if limit and category:
            Budget.objects.create(user=request.user, limit=limit, category=category)

        return redirect('budget.index')

    return render(request, 'budget/index.html', {
        'budgets': budgets,
        'template_data': template_data,
    })
