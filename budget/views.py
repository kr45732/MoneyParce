from django.shortcuts import render, redirect, get_object_or_404
from MoneyParce.models import Expense, Budget
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal

@login_required
def index(request):
    template_data = {'title': 'MoneyParce - Budget', 'section': 'Budget'}

    budgets = Budget.objects.filter(user=request.user)

    # Calculate amount spent and percent used for each budget
    for budget in budgets:
        if budget.category == "ALL":
            expenses = Expense.objects.filter(user=request.user)
        else:
            expenses = Expense.objects.filter(user=request.user, category=budget.category)

        total_spent = sum(exp.amount for exp in expenses)

        if budget.limit > Decimal('0'):
            budget.percent_used = round((total_spent / budget.limit) * Decimal('100.0'), 2)
        else:
            budget.percent_used = Decimal('0.0')

        budget.amount_spent = total_spent

    if request.method == 'POST':
        limit = Decimal(request.POST.get('limit'))
        category = request.POST.get('category')

        if limit and category:
            budget, created = Budget.objects.get_or_create(
                user=request.user,
                category=category,
                defaults={'limit': limit}
            )
            if not created:
                budget.limit = limit
                budget.save()

            # After creating/updating budget, re-calculate spending
            if budget.category == "ALL":
                expenses = Expense.objects.filter(user=request.user)
            else:
                expenses = Expense.objects.filter(user=request.user, category=budget.category)

            total_spent = sum(exp.amount for exp in expenses)

            if budget.limit > Decimal('0'):
                percent_spent = (total_spent / budget.limit) * Decimal('100.0')

                if percent_spent >= 100:
                    messages.error(request, f"🔥 You are already over your {budget.category} budget!")
                elif percent_spent >= 90:
                    messages.warning(request, f"⚠️ You have already used 90% of your {budget.category} budget.")
                elif percent_spent >= 75:
                    messages.warning(request, f"⚠️ You have already used 75% of your {budget.category} budget.")

        return redirect('budget.index')

    return render(request, 'budget/index.html', {
        'budgets': budgets,
        'template_data': template_data,
    })

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    budget.delete()
    return redirect('budget.index')
