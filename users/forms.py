from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EmailConfirmationForm(forms.Form):
    code = forms.CharField(label='Код, отправленный на почту', widget=forms.TextInput(attrs={'class': 'form-control'}))
