from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TournamentStartForm
from ..models import Tournament


def start_tournament(request, tt_slug):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    if request.method == 'POST':
        start_form = TournamentStartForm(request.POST)
        if start_form.is_valid():
            tournament.status = start_form.cleaned_data['status']
            tournament.save()
            if start_form.cleaned_data['status'] == 'act':
                tournament.create_tours()
            return redirect('tournaments-list')
    else:
        start_form = TournamentStartForm()
    return render(
        request,
        'tournament_start_form.html',
        {'tournament': tournament, 'start_form': start_form, }
    )
