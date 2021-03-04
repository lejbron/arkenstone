from django.contrib.auth.models import User
from django.shortcuts import render

from tournaments.models import Tournament


def index(request):
    """View function for home page of site."""

    players_amount = User.objects.all().count()
    tournaments_amount = Tournament.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_visits': num_visits,
        'players_amount': players_amount,
        'tournaments_amount': tournaments_amount,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
