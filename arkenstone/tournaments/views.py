from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import TournamentRegisterForm, TournamentStartForm
from .models import Match, PlayerStats, Tour, Tournament


def tournament_detail_view(request, tournament):
    '''
    Отображение детальной информации о турнире.

    Attributes:
        tournament: Выбранный турнир.
        players_stat: Текущие результаты турнира. Статусы турнира: ['act', 'fin'].'
    '''
    tournament = get_object_or_404(Tournament, title=tournament)

    context = {
        'tournament': tournament,
        'players_stat': tournament.registered_players,
        }

    return render(request, 'tournament_detail.html', context=context)


def tournaments_list_view(request):
    '''
    Отображение списка турниров.

    Attributes:
        tournaments_list: Список турниров. Статусы турнира: ['ann', 'reg', 'creg', 'act'].
        tournaments_reglist: Список значений id туриниров, на которые зараегистрирован
                             залогиненый пользователь.

    '''
    tournaments_list = get_list_or_404(Tournament)

    try:
        players = PlayerStats.objects.filter(player=request.user)
        tournaments_reglist = players.values_list('tournament', flat=True)
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tournaments_list': tournaments_list,
        'tournaments_reglist': tournaments_reglist,
        }

    return render(request, 'tournaments_list.html', context=context)


def register_on_tournament(request, tournament):
    '''
    Форма регистрации на турнир.

    Attributes:
        tournament: Выбранный турнир.
        reg_form: Форма регистрации.
        player_stat: Статистика игрока на выбранном турнире.
    '''
    tournament = get_object_or_404(Tournament, title=tournament)

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


def tour_detail_view(request, tournament, tour_pk):
    '''
    Отображение детальной информации о туре.

    Attributes:
        tour: Выбранный тур.
        player_stat: Текущие результаты тура(ВРЕМЕННО ТУРНИРА). Статусы туринра: ['act', 'fin'].
        matches: Список матчей тура. Статусы тура: ['prd','act','fin']
    '''
    tour = get_object_or_404(Tour, id=tour_pk)

    try:
        players_stat = PlayerStats.objects.filter(tournament=tour.tournament)
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tour': tour,
        'players_stat': players_stat,
        }

    return render(request, 'tour_detail.html', context=context)


def match_detail_view(request, tournament, tour_pk, match_pk):
    '''
    Отображение детальной информации о матче.

    Attributes:
        match: Выбранный матч.
    '''
    match = get_object_or_404(Match, id=match_pk)
    context = {
        'match': match,
        }

    return render(request, 'match_detail.html', context=context)


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
    registered_players = tour.tournament.registered_players.values_list('player', flat=True)
    data = request.POST or None
#   if tour.tour_status == 'crt':
#        tour.setup_pairs()

    MatchesFormSet = inlineformset_factory(
        Tour,
        Match,
        fields=('opp1', 'opp2',),
        extra=0,
        can_delete=False,)
    formset = MatchesFormSet(
        data,
        instance=tour,)
    for form in formset:
        form.fields['opp1'].queryset = User.objects.filter(id__in=registered_players)
        form.fields['opp2'].queryset = User.objects.filter(id__in=registered_players)

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
