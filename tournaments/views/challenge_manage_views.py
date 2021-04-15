from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect

from tournaments.models import Challenge, Tournament


@login_required
def challenge_create(request, tt_slug, player_id):
    opponent = get_object_or_404(User, id=player_id)
    if request.user != opponent:
        tournament = get_object_or_404(Tournament, tt_slug=tt_slug)
        Challenge.objects.get_or_create(
            tournament=tournament,
            user=request.user,
            opponent=opponent,
        )
    return redirect('player-detail', player_id)


@login_required
def challenge_cancel(request, tt_slug, player_id):
    challenge = get_object_or_404(Challenge, tournament__tt_slug=tt_slug, user=request.user, opponent_id=player_id)
    challenge.delete()
    return redirect('player-detail', player_id)


@login_required
def challenge_accept(request, tt_slug, player_id):
    # добавить поле со статусом вызова - ожидается, принят, отказ
    return redirect('player-detail', player_id)


@login_required
def challenge_refuse(request, tt_slug, player_id):
    get_object_or_404(Challenge, tournament__tt_slug=tt_slug, user=request.user, opponent_id=player_id)
    # Здесь не удалять вызов, а изменять статус.
    return redirect('player-detail', player_id)
