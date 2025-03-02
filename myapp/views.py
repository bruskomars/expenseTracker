from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.db.models import Sum
import datetime
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

# Create your views here.
@login_required(login_url='login')
def index(request):
    form = ExpenseForm()
    expenses = Expense.objects.filter(user=request.user)
    sum_expenses = expenses.aggregate(Sum('amount'))

    #Calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = expenses.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    daily_sums = expenses.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    cat_sums = expenses.filter().values('category').order_by('category').annotate(sum=Sum('amount'))

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('index')

    context = {
        'form':form,
        'expenses': expenses,
        'sum_expenses':sum_expenses,
        'yearly_sum':yearly_sum,
        'daily_sums':daily_sums,
        'cat_sums':cat_sums,
    }
    return render(request, "myapp/index.html", context)

def edit(request, id):
    item = get_object_or_404(Expense, id=id)
    form = ExpenseForm(instance=item)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'myapp/edit.html', context)

def delete(request, id):
    item = get_object_or_404(Expense, id=id)
    item.delete()
    return redirect('index')

def login_user(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                return redirect('index')

            else:
                return HttpResponse("<h1>Invalid credentials</h1>")

    context = {
        'form': form,
    }
    return render(request, 'myapp/login.html', context)

def logout_user(request):
    logout(request)

    return redirect('index')

def register_user(request):
    form =RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            return redirect('index')

    context = {
        'form': form,
    }

    return render(request, 'myapp/register.html', context)