from django.db import models
from django.contrib.auth.models import User
from enum import Enum

expense_categories = [
    ("OTHER", "Other"),
    ("FOOD", "Food"),
    ("TRANSPORT", "Transport"),
    ("ENTERTAINMENT", "Entertainment"),
    ("UTILITIES", "Utilities"),
    ("HEALTH", "Health"),
]

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=expense_categories + [("ALL", "All")],
        default="All",
    )

    def __str__(self):
        return f"{self.user.username}'s Budget: ${self.limit}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(
        max_length=50,
        choices=expense_categories,
        default="Other",
    )

    def __str__(self):
        return f"{self.user.username}'s Budget for {self.category}: ${self.limit}"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description}: +${self.amount}"