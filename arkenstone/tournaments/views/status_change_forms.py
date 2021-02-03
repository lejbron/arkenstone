from django.shortcuts import get_object_or_404, redirect

from ..models import Tournament


def start_tournament(request, tt_slug):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    tournament.status = 'act'
    tournament.save()
    tournament.create_tours()
    return redirect('tournament-detail', tournament.tt_slug)

