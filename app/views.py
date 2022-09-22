from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm


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


