from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    nickname = forms.CharField(
        label='nickname',
        help_text='Your tournament name')
    army = forms.CharField(
        label='army',
        help_text='Enter if you have one')
    birth_date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'nickname', 'army', 'birth_date', 'password1', 'password2', )
