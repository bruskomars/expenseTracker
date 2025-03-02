from django import forms
from .models import *
from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name', 'amount', 'category',)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            return forms.ValidationError("Password do not match")

        return self.cleaned_data['password2']