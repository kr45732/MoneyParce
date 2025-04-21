from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import CustomUserCreationForm, CustomErrorList, CustomUserResetForm
from .models import CustomUser

from django.contrib.auth.models import User

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('/')


def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            security_answer_1 = form.cleaned_data.get('security_1')
            security_answer_2 = form.cleaned_data.get('security_2')
            security_answer_3 = form.cleaned_data.get('security_3')
            user = User.objects.get(username=username)
            user_data = CustomUser.objects.create(user=user, security_answer_1=security_answer_1,
                                                  security_answer_2=security_answer_2,
                                                  security_answer_3=security_answer_3)
            user_data.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})


def reset(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        template_data['form'] = CustomUserResetForm()
        return render(request, 'accounts/reset.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserResetForm(request.POST, error_class=CustomErrorList)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                user = User.objects.get(username=username)
                custom_user = CustomUser.objects.get(user_id=user.id)

                if form.cleaned_data.get('security_1') == custom_user.security_answer_1 and \
                        form.cleaned_data.get('security_2') == custom_user.security_answer_2 and \
                        form.cleaned_data.get('security_3') == custom_user.security_answer_3:
                    user.set_password(form.cleaned_data.get("password"))
                    user.save()
                    return redirect('accounts.login')
                else:
                    messages.error(request, 'One or more of the security questions are incorrect!')
            except (CustomUser.DoesNotExist, User.DoesNotExist):
                messages.error(request, 'Provided user does not exist!')

        template_data['form'] = form
        return render(request, 'accounts/reset.html', {'template_data': template_data})
