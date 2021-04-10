from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render


def player_detail_view(request, player_id):
    """
    View-функция отображения детальной информации об игроке.

    Attribures:
        player_info: содержит информацию о статистике игрока на турнирах (PlayerStats).
    """
    player = get_object_or_404(User, id=player_id)

    context = {
        'player': player,
        'player_info': player.tt_stats.all(),
        }

    return render(request, 'player_detail.html', context=context)
