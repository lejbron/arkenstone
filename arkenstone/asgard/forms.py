from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from players.models import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date',)
