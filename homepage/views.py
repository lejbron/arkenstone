from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, render

from tournaments.models import Tournament


def index(request):
    """View function for home page of site."""

    users_amount = User.objects.all().count()
    tournaments_amount = Tournament.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
        'users_amount': users_amount,
        'tournaments_amount': tournaments_amount,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def users_list_view(request):
    """
    View-функция отображения всех зарегистрированных на сайте пользователей.
    """
    users_list = get_list_or_404(User.objects.all().select_related('profile'))

    context = {'users_list': users_list, }

    return render(request, 'users_list.html', context=context)
