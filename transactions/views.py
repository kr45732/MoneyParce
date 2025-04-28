from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta, date

from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from plaid import Configuration
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.plaid_error import PlaidError
from plaid.model.products import Products
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

import env.env
from MoneyParce.forms import ExpenseForm, IncomeForm
from MoneyParce.models import Expense, Income, Budget

from django.contrib import messages
from django.db.models import Sum

#from MoneyParce.utils import check_budget_status


@login_required

def index(request):
    template_data = {'title': 'Transactions'}

    expense_form = ExpenseForm()
    income_form = IncomeForm()

    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    return render(request, 'transactions/index.html', {
        'expense_form': expense_form,
        'income_form': income_form,
        'expenses': expenses,
        'incomes': incomes,
        'template_data': template_data
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        if 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()

                check_budget_status(request, expense)
        elif 'add_income' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                income.save()

    return redirect("transactions.index")

def check_budget_status(request, expense):
    try:
        budget = Budget.objects.get(user=request.user, category=expense.category)
    except Budget.DoesNotExist:
        return

    total_spent = Expense.objects.filter(user=request.user, category=expense.category).aggregate(total=Sum('amount'))['total'] or 0

    percent_used = (total_spent / budget.limit) * 100 if budget.limit > 0 else 0

    if percent_used >= 100:
        messages.error(request, f"🔥 You are OVER your budget for {budget.category}!")
    elif percent_used >= 75:
        messages.warning(request, f"⚠️ You are close to your budget limit for {budget.category}!")


@login_required
def remove_transaction(request, transaction_id, transaction_type):
    if transaction_type == 'expense':
        transaction = get_object_or_404(Expense, id=transaction_id, user=request.user)
    elif transaction_type == 'income':
        transaction = get_object_or_404(Income, id=transaction_id, user=request.user)
    else:
        raise Http404("Transaction type not found.")

    transaction.delete()
    return redirect("transactions.index")

def create_link_token(request):
    # TODO: enforce get request method?
    client_user_id = str(request.user.id)  # Ensure client_user_id is a string

    # Configure the Plaid client
    configuration = Configuration(
        host=env.env.PLAID_ENV,
        api_key={
            'clientId': env.env.PLAID_CLIENT_ID,
            'secret': env.env.PLAID_SECRET,
        }
    )
    api_client = plaid_api.ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)

    response = client.categories_get({})
    categories = response.categories

    print(categories)

    link_token_request = LinkTokenCreateRequest(
        products=[Products("auth"), Products("transactions")],
        client_name="MoneyParce",
        country_codes=[CountryCode('US')],
        # redirect_uri='http://localhost:8000/oauth/callback',
        language='en',
        webhook='http://localhost:8000/webhook',
        user=LinkTokenCreateRequestUser(
            client_user_id=client_user_id
        )
    )
    response = client.link_token_create(link_token_request)
    return JsonResponse({'link_token': response.link_token})

def exchange_public_token(request):
    if request.method == 'POST':
        try:
            # Parse the public_token from the request body
            data = json.loads(request.body)
            public_token = data.get('public_token')

            if not public_token:
                return JsonResponse({'error': 'Missing public_token'}, status=400)

            # Configure the Plaid client
            configuration = Configuration(
                host=env.env.PLAID_ENV,
                api_key={
                    'clientId': env.env.PLAID_CLIENT_ID,
                    'secret': env.env.PLAID_SECRET,
                }
            )
            api_client = plaid_api.ApiClient(configuration)
            client = plaid_api.PlaidApi(api_client)

            # Exchange the public_token for an access_token
            exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
            exchange_response = client.item_public_token_exchange(exchange_request)

            access_token = exchange_response.access_token

            # ------------- Use access token to get transactions ----------

            start_date: date = (datetime.now() - timedelta(days=30)).date()
            end_date: date = datetime.now().date()

            # Create the request
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date= start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(
                    count=100,  # Number of transactions to fetch
                    offset=0    # Offset for pagination
                )
            )

            response = client.transactions_get(request)
            transactions = response.transactions

            return JsonResponse({'transactions': [t.to_dict() for t in transactions]})

        except PlaidError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)