from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import ProfileForm, SignUpForm, UpdateUserForm


@transaction.atomic
def signup(request):
    """
    View-функция регистрации пользователя.
    Модель профиля обновляется вместе с моделью пользователя засчет настроенного сигнала.

    Attributes:
        user_form: Форма регистрации пользователя.
    """
    data = request.POST or None

    user_form = SignUpForm(data)
    if user_form.is_valid():
        user = user_form.save()
        user.refresh_from_db()
        user.profile.birth_date = user_form.cleaned_data.get('birth_date')
        user.save()
        raw_password = user_form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        login(request, user)
        return redirect('index')

    context = {
        'user_form': user_form,
    }

    return render(request, 'signup.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    """
    View-функция обновления данных о пользователе.

    Attributes:
        user_form: Форма обновления данных о пользователе.
        profile_form: Форма обновления профиля пользователя.
    """
    data = request.POST or None
    user_form = UpdateUserForm(data, instance=request.user)
    profile_form = ProfileForm(data, instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('index')

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'update_profile.html', context)
