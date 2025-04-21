from collections import defaultdict
from datetime import timedelta, date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from MoneyParce.models import Expense, Income


def get_date_range(filter_option):
    today = date.today()

    if filter_option == "last_7_days":
        return today - timedelta(days=6), today
    elif filter_option == "this_month":
        return today.replace(day=1), today
    elif filter_option == "last_month":
        first = today.replace(day=1)
        last_month_end = first - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        return last_month_start, last_month_end
    else:
        return None, None
@login_required
def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'

    date_filter = request.GET.get("date_filter", "this_month")
    group_by = request.GET.get("group_by", "daily")

    start_date, end_date = get_date_range(date_filter)

    # Filter user-specific data
    expenses = Expense.objects.filter(user=request.user)
    income = Income.objects.filter(user=request.user)

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])
        income = income.filter(date__range=[start_date, end_date])

    # Pie Chart (Category)
    category_data = (
        expenses
        .values("category")
        .annotate(total=Sum("amount"))
    )
    pie_chart_data = [["Category", "Amount"]]
    for item in category_data:
        pie_chart_data.append([item['category'], float(item['total'])])

    def group_queryset(queryset, group_by):
        grouped = defaultdict(float)

        for obj in queryset:
            date = obj.date

            if group_by == "weekly":
                # Normalize to Monday of that week
                date = date - timedelta(days=date.weekday())
            elif group_by == "monthly":
                date = date.replace(day=1)
            else:
                # Daily: leave the date as is
                pass

            grouped[date] += float(obj.amount)

        # Sort the result by date
        return sorted(grouped.items())

    line_chart_data_expenses = [["Date", "Expense"]]
    for date, total in group_queryset(expenses, group_by):
        line_chart_data_expenses.append([date.strftime("%Y-%m-%d"), total])

    line_chart_data_income = [["Date", "Income"]]
    for date, total in group_queryset(income, group_by):
        line_chart_data_income.append([date.strftime("%Y-%m-%d"), total])

    context = {
        "pie_chart_data": pie_chart_data,
        "line_chart_data_expenses": line_chart_data_expenses,
        "line_chart_data_income": line_chart_data_income,
        "date_filter": date_filter,
        "group_by": group_by,
    }

    return render(request, 'overview/index.html', context)