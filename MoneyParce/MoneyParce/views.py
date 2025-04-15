from django.shortcuts import render
from .models import Expense
from .utils import check_budget_status

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login, authenticate

def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    warning = check_budget_status(request.user)
    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'warning': warning,
    })

def SignUp(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = UserCreationForm()
        return render(request, 'MoneyParce/SignUp.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.index')
        else:
            template_data['form'] = form
            return render(request, 'MoneyParce/SignUp.html',
                {'template_data': template_data})
        
def Login(request):
    template_data = {'title': 'Login'}
    
    if request.method == 'GET':
        return render(request, 'MoneyParce/Login.html', {'template_data': template_data})
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'MoneyParce/Login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('dashboard')