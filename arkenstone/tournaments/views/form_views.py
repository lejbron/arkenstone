from django.shortcuts import get_object_or_404, redirect, render

from ..forms import (MatchesPairsFormSet, MatchesResultsFormSet,
                     TournamentRegisterForm, TournamentStartForm)
from ..models import PlayerStats, Tour, Tournament


def register_on_tournament(request, tt_title):
    '''
    Форма регистрации на турнир.

    Attributes:
        tournament: Выбранный турнир.
        reg_form: Форма регистрации.
        player_stat: Статистика игрока на выбранном турнире.
    '''
    tournament = get_object_or_404(Tournament, title=tt_title)

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


def start_tournament(request, tt_title):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tournament = get_object_or_404(Tournament, title=tt_title)

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


def input_tour_pairs(request, tour_id):
    '''
    Форма корректировки парингов. Доступна только организаторам.
    '''
    tour = get_object_or_404(Tour, pk=tour_id)
    data = request.POST or None

    formset = MatchesPairsFormSet(
        data,
        instance=tour,)
    for form in formset:
        form.fields['opp1'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)
        form.fields['opp2'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        tour.tour_status = 'prd'
        tour.save()
        return redirect(
            'tour-detail',
            str(tour.tournament),
            str(tour.id)
        )

    context = {
        'formset': formset,
        'tour': tour,
    }

    return render(request, 'tour_matches_setup_form.html', context)


def input_tour_results(request, tour_id):
    '''
    Форма корректировки парингов. Доступна только организаторам.
    '''
    tour = get_object_or_404(Tour, pk=tour_id)
#    registered_players = tour.tournament.registered_players.values_list('player', flat=True)
    data = request.POST or None
#   if tour.tour_status == 'crt':
#        tour.setup_pairs()

    formset = MatchesResultsFormSet(
        data,
        instance=tour,)
    for form in formset:
        form.fields['opp1'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)
        form.fields['opp2'].queryset = PlayerStats.objects.filter(tournament=tour.tournament)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
#        tour.tour_status = 'fin'
#       tour.save()
        if tour.tour_status == 'fin':
            tour.update_tour_results()
        return redirect(
            'tour-detail',
            str(tour.tournament),
            str(tour.id)
        )

    context = {
        'formset': formset,
        'tour': tour,
    }

    return render(request, 'tour_matches_setup_form.html', context)
