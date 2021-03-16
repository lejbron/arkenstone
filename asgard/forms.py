from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from players.models import Profile


class SignUpForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    birth_date = forms.DateField(
        required=False,
        help_text='Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date')


class UpdateUserForm(forms.ModelForm):
    """
    Форма обновеления информации о пользователе.
    """
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    """
    Форма профиля пользователя.
    """
    class Meta:
        model = Profile
        fields = ('birth_date',)
