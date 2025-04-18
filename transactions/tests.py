from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from MoneyParce.models import Expense, Income


class TransactionViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_expense(self):
        url = reverse('add_transaction')

        response = self.client.post(url, {
            'amount': '50.00',
            'description': 'Groceries',
            'category': 'FOOD',
            'add_expense': True,
        })
        self.assertEqual(response.status_code, 302) # 302 as it redirects after saving
        self.assertEqual(Expense.objects.count(), 1)
        expense = Expense.objects.first()
        self.assertEqual(expense.amount, 50.00)
        self.assertEqual(expense.description, 'Groceries')
        self.assertEqual(expense.category, 'FOOD')

    def test_add_income(self):
        url = reverse('add_transaction')

        response = self.client.post(url, {
            'amount': '100.00',
            'description': 'Salary',
            'add_income': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Income.objects.count(), 1)
        income = Income.objects.first()
        self.assertEqual(income.amount, 100.00)
        self.assertEqual(income.description, 'Salary')