# from django.contrib.auth.models import User
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import TournamentRegisterForm
from .models import PlayerStats, Tour, Tournament


def tournament_detail_view(request, pk):
    """Функция отображения детальной информации о турнире."""
    tournament = get_object_or_404(Tournament, id=pk)

    tours_list = Tour.objects.filter(tournament=tournament)

    # queryset = PlayerStats.objects.filter(tournament__exact=tournament).\
    #    order_by('-tournament_points', '-difference', '-game_points')
    # players_stat = get_list_or_404(queryset)
    players_stat = PlayerStats.objects.filter(tournament=tournament).\
        order_by('-tournament_points', '-difference', '-game_points')

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


def register_on_tournament(request, pk):
    """Функция отображения формы регистрации на турнир."""
    tournament = Tournament.objects.get(id=pk)

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


def tour_detail_view(request, pk):
    """Функция отображения детальной информации о туре."""
    tour = get_object_or_404(Tour, id=pk)

    players_stat = PlayerStats.objects.filter(tournament=tour.tournament).\
        order_by('-tournament_points', '-difference', '-game_points')

    context = {
        'tour': tour,
        'players_stat': players_stat,
        }

    return render(request, 'tour_detail.html', context=context)
