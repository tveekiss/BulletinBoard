from random import randint

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import OneTimeCode
from .forms import UserRegisterForm, UserAuthenticationForm, EmailConfirmationForm




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            while True:
                code = randint(10000, 99999)
                if OneTimeCode.objects.filter(code=code).exists():
                    continue
                break
            OneTimeCode.objects.create(user=user, code=code)
            print(code)
            request.session['code'] = str(code)
            return redirect('email-confirm')
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
            print(user)
            messages.success(request, 'Вы успешно вошли в свой аккаунт!')
            while True:
                code = randint(10000, 99999)
                if OneTimeCode.objects.filter(code=code).exists():
                    continue
                break
            OneTimeCode.objects.create(user=user, code=code)
            print(code)
            request.session['code'] = str(code)
            return redirect('email-confirm')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserAuthenticationForm()
    return render(request, 'users/login.html', {'title': 'Вход', 'form': form})


def email_confirm(request):
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code']
            code = request.session.get('code')
            print(user_code, code)
            if code == user_code:
                messages.success(request, 'Вы успешно вошли в аккаунт!')
                db_code = OneTimeCode.objects.get(code=code)
                user = db_code.user
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверный код')
        else:
            messages.error(request, 'Ошибка ввода')
    else:
        form = EmailConfirmationForm()
    return render(request, 'users/code_confirm.html', context={'title': 'Подтверждение почты', 'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из своего аккаунта!')
    return redirect('home')
