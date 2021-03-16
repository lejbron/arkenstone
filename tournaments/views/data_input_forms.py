from django.shortcuts import get_object_or_404, redirect, render

from players.models import PlayerStats
from tournaments.forms import MatchesResultsFormSet, TournamentRegisterForm
from tournaments.models import Tour, Tournament


def register_on_tournament(request, tt_slug):
    """
    View-функция формы регистрации на турнир.

    Attributes:
        tournament: Выбранный турнир.
        reg_form: Форма регистрации.
        player_stat: Статистика игрока на выбранном турнире.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    data = request.POST or None
    reg_form = TournamentRegisterForm(data)

    if reg_form.is_valid():
        player_stat = reg_form.save(commit=False)
        player_stat.tournament = tournament
        player_stat.player = request.user
        player_stat.save()
        return redirect('index')

    context = {
        'tournament': tournament,
        'reg_form': reg_form,
    }

    return render(request, 'tournament_reg_form.html', context)


def input_tour_results(request, tour_slug):
    """
    View-функция формы внесения результатов тура.

    Attributes:
        tour: Тур, для которого вносятся результаты.
        formset: Набор форм внесения результатов матча.
    """
    tour = get_object_or_404(Tour, tour_slug=tour_slug)
    data = request.POST or None

    formset = MatchesResultsFormSet(data, instance=tour)
    for form in formset:
        form.fields['opp1'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)
        form.fields['opp2'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)

    if formset.is_valid():
        formset.save()
        if tour.tour_status == 'fin':
            tour.update_tour_results()
        return redirect('tour-detail', tour.tour_slug)

    context = {
        'tour': tour,
        'formset': formset,
    }

    return render(request, 'tour_matches_setup_form.html', context)
