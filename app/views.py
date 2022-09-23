from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import CreateView

from .models import Order
from .forms import SignUpForm, NewOrderForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def profile(request):
    context = {

    }
    return render(request, 'profile.html', context=context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def index(request):
    context = {

    }
    return render(request, 'index.html', context=context)


@login_required
def ordercreate(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.status = 'н'
            stock.save()
            return redirect('myorders')
    else:
        form = NewOrderForm()
    return render(request, 'order_form.html', {'form': form})
