from django.contrib import admin
from .models import Budget, Expense, Income

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display  = ("user", "limit", "category")
    list_filter   = ("category",)
    search_fields = ("user__username",)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display  = ("user", "amount", "category", "date")
    list_filter   = ("category", "date")
    search_fields = ("description", "user__username")

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display  = ("user", "amount", "date")
    list_filter   = ("date",)
    search_fields = ("description", "user__username")