# from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, render

from tournaments.models import PlayerStats


def player_detail_view(request, pk):
    """
    View-функция отображения детальной информации об игроке.

    Attribures:
        player_info: содержит информацию о статистике игрока на турнирах (PlayerStats).
    """
    player_info = get_list_or_404(PlayerStats.objects.filter(player_id=pk))

    context = {
        'player': player_info[0].player,
        'player_info': player_info,
        }

    return render(request, 'player_detail.html', context=context)
