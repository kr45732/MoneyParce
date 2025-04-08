def check_budget_status(user):
    try:
        budget = Budget.objects.get(user=user)
        total_spent = Expense.objects.filter(user=user).aggregate(models.Sum('amount'))['amount__sum'] or 0

        percent_spent = (total_spent / budget.limit) * 100

        if percent_spent >= 100:
            return "🚨 You've exceeded your budget!"
        elif percent_spent >= 90:
            return "⚠️ You're at 90% of your budget."
        elif percent_spent >= 75:
            return "⚠️ You're at 75% of your budget."
        else:
            return None
    except Budget.DoesNotExist:
        return "No budget set yet."
