from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, render

from tournaments.models import PlayerStats


def player_detail_view(request, pk):
    """Функция отображения детальной информации об игроке."""
    player_info = get_list_or_404(PlayerStats.objects.filter(player_id=pk))

    context = {
        'player': player_info[0].player,
        'player_info': player_info,
        }

    return render(request, 'player_detail.html', context=context)


def players_list_view(request):
    """Функция отображения списка игроков."""
    players_list = get_list_or_404(User.objects.all().select_related('profile'))

    context = {'players_list': players_list, }

    return render(request, 'players_list.html', context=context)
