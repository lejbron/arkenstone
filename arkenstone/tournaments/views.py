# from django.contrib.auth.models import User
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import TournamentRegisterForm
from .models import PlayerStats, Tour, Tournament


def tournament_detail_view(request, tournament):
    """Функция отображения детальной информации о турнире."""
    tournament = get_object_or_404(Tournament, title=tournament)

    try:
        tours_list = Tour.objects.filter(tournament=tournament)
        players_stat = PlayerStats.objects.filter(tournament=tournament).\
            order_by('-tournament_points', '-difference', '-game_points')
    except Tour.DoesNotExist:
        pass
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tournament': tournament,
        'tours_list': tours_list,
        'players_stat': players_stat,
        }

    return render(request, 'tournament_detail.html', context=context)


def tournaments_list_view(request):
    """Функция отображения списка турниров."""
    tournaments_list = get_list_or_404(Tournament)

    try:
        players = PlayerStats.objects.filter(player=request.user)
        tournaments_reglist = players.values_list('tournament', flat=True)
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tournaments_list': tournaments_list,
        'tournaments_reglist': tournaments_reglist,
        }

    return render(request, 'tournaments_list.html', context=context)


def register_on_tournament(request, tournament):
    """Функция отображения формы регистрации на турнир."""
    tournament = get_object_or_404(Tournament, title=tournament)

    if request.method == 'POST':
        reg_form = TournamentRegisterForm(request.POST)
        if reg_form.is_valid():
            player = reg_form.save()
            player.tournament = tournament
            player.player = request.user
            player.save()
            return redirect('index')
    else:
        reg_form = TournamentRegisterForm()
    return render(request, 'tournament_reg_form.html', {'tournament': tournament, 'reg_form': reg_form, })


def tour_detail_view(request, tournament, tour_pk):
    """Функция отображения детальной информации о туре."""
    tour = get_object_or_404(Tour, id=tour_pk)

    try:
        players_stat = PlayerStats.objects.filter(tournament=tour.tournament).\
            order_by('-tournament_points', '-difference', '-game_points')
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tour': tour,
        'players_stat': players_stat,
        }

    return render(request, 'tour_detail.html', context=context)
