from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'class': 'form-control',
                                      'placeholder': 'Введите ваше имя пользователя'})
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control',
                                          'placeholder': 'Введите ваше пароль'})
    )

    class Mena:
        model = User
        fields: list[str] = ['username', 'password']
