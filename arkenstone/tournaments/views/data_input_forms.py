from django.shortcuts import get_object_or_404, redirect, render

from ..forms import MatchesResultsFormSet, TournamentRegisterForm
from ..models import PlayerStats, Tour, Tournament


def register_on_tournament(request, tt_slug):
    '''
    Форма регистрации на турнир.

    Attributes:
        tournament: Выбранный турнир.
        reg_form: Форма регистрации.
        player_stat: Статистика игрока на выбранном турнире.
    '''
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    if request.method == 'POST':
        reg_form = TournamentRegisterForm(request.POST)
        if reg_form.is_valid():
            player_stat = reg_form.save()
            player_stat.tournament = tournament
            player_stat.player = request.user
            player_stat.save()
            return redirect('index')
    else:
        reg_form = TournamentRegisterForm()
    return render(request, 'tournament_reg_form.html', {'tournament': tournament, 'reg_form': reg_form, })


def input_tour_results(request, tour_slug):
    '''
    Форма корректировки парингов. Доступна только организаторам.
    '''
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    data = request.POST or None

    formset = MatchesResultsFormSet(
        data,
        instance=tour,)
    for form in formset:
        form.fields['opp1'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)
        form.fields['opp2'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        if tour.tour_status == 'fin':
            tour.update_tour_results()
        return redirect('tour-detail', tour.tour_slug)

    context = {
        'formset': formset,
        'tour': tour,
    }

    return render(request, 'tour_matches_setup_form.html', context)
