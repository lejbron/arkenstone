from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from tournaments.models import Challenge


def player_detail_view(request, player_id):
    """
    View-функция отображения детальной информации об игроке.

    Attribures:
        player_info: содержит информацию о статистике игрока на турнирах (PlayerStats).
    """
    player = get_object_or_404(User, id=player_id)
    # Проверить на анонима
    all_challenges = Challenge.objects.filter(opponent_id=player_id)
    user_challenges = all_challenges.filter(user=request.user)
    context = {
        'player': player,
        'player_info': player.tt_stats.all(),
        'all_challenges': all_challenges,
        'user_challenges': user_challenges,
        }

    return render(request, 'player_detail.html', context=context)
