from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title': 'Регистрация', 'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в свой аккаунт!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserAuthenticationForm()
    return render(request, 'users/login.html', {'title': 'Вход', 'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из своего аккаунта!')
    return redirect('home')
