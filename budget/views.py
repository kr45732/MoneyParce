from django.shortcuts import render, redirect
from MoneyParce.models import Budget
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    user = request.user

    if request.method == 'POST':
        limit = request.POST.get('limit')
        category = request.POST.get('category')

        budget, created = Budget.objects.get_or_create(
            user=user,
            category=category,
            defaults={'limit': limit}
        )
        if not created:
            budget.limit = limit
            budget.save()

        return redirect('budget.index')

    user_budgets = Budget.objects.filter(user=user)
    all_budgets = Budget.objects.all()

    template_data = {
        'title': 'MoneyParce - Budget',
        'section': 'Budget',
        'user_budgets': user_budgets,
        'all_budgets': all_budgets,
        'category_choices': Budget._meta.get_field('category').choices,
    }
    return render(request, 'budget/index.html', template_data)
