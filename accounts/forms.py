from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))


class CustomUserCreationForm(UserCreationForm):
    security_1 = forms.CharField(
        label="Security Question #1",
        help_text="What is your mother's maiden name?",
        strip=False,
    )
    security_2 = forms.CharField(
        label="Security Question #2",
        help_text="What year was your father born?",
        strip=False,
    )
    security_3 = forms.CharField(
        label="Security Question #3",
        help_text="What's your favorite pet?",
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2', "security_1", 'security_2', 'security_3']:
            if fieldname not in ["security_1", 'security_2', 'security_3']:
                self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'security_1', 'security_2', 'security_3')


class CustomUserResetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomUserResetForm, self).__init__(*args, **kwargs)

        self.fields["username"] = forms.CharField(
            label="Username",
            strip=False,
        )
        self.fields["password"] = forms.CharField(
            label="New Password",
            widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
            help_text=password_validation.password_validators_help_text_html(),
            strip=False,
        )
        self.fields["security_1"] = forms.CharField(
            label="Security Question #1",
            help_text="What is your mother's maiden name?",
            strip=False,
        )
        self.fields["security_2"] = forms.CharField(
            label="Security Question #2",
            help_text="What year was your father born?",
            strip=False,
        )
        self.fields["security_3"] = forms.CharField(
            label="Security Question #3",
            help_text="What's your favorite pet?",
            strip=False,
        )

        for fieldname in ['username', 'password', "security_1", 'security_2', 'security_3']:
            if fieldname not in ["security_1", 'security_2', 'security_3']:
                self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
