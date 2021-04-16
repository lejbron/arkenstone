from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, get_object_or_404, redirect

from players.models import PlayerStats
from tournaments.decorators import superviser_check
from tournaments.models import Tournament


@login_required
@superviser_check
def player_delete(request, tt_slug, player_id):
    """
    View-функция удаления игрока из турнира.
    """
    player_stat = get_object_or_404(PlayerStats, tournament__tt_slug=tt_slug, player__id=player_id)
    player_stat.delete()
    return redirect('tournament-detail', tt_slug)


@login_required
@superviser_check
def player_add_bot(request, tt_slug):
    """
    View-функция добавления бота на турнир.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)
    if not tournament.reg_is_open_or_close:
        raise PermissionDenied

    count = tournament.players.count()
    if count % 2 == 0:
        return redirect('tournament-detail', tt_slug)

    proxy_bots = get_list_or_404(User, profile__proxy_bot=True)
    for bot in proxy_bots:
        if not bot.tt_stats.filter(tournament=tournament).exists():
            PlayerStats.objects.create(
                tournament=tournament,
                player=bot,
            )
            return redirect('tournament-detail', tt_slug)
    return redirect('tournament-detail', tt_slug)
