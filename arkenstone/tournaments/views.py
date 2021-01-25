# from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import PlayerStats, Tournament


def tournament_detail_view(request, pk):
    """Функция отображения детальной информации об игроке."""
    tournament = get_object_or_404(Tournament, id=pk)

    queryset = PlayerStats.objects.filter(tournament__exact=tournament).\
        order_by('-tournament_points', '-difference', '-game_points')
    players_stat = get_list_or_404(queryset)

    context = {
        'tournament': tournament,
        'players_stat': players_stat,
        }

    return render(request, 'tournament_detail.html', context=context)


def tournaments_list_view(request):
    """Функция отображения списка игроков."""
    tournaments_list = get_list_or_404(Tournament)

    context = {'tournaments_list': tournaments_list, }

    return render(request, 'tournaments_list.html', context=context)
