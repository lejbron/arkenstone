# from django.contrib.auth.models import User
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import TournamentRegisterForm, TournamentStartForm
from .models import Match, PlayerStats, Tour, Tournament


def tournament_detail_view(request, tournament):
    '''
    Отображение детальной информации о турнире.

    Attributes:
        tournament: Выбранный турнир.
        tours_list: Список туров.
        players_stat: Текущие результаты турнира. Статусы турнира: ['act', 'fin'].'
    '''
    tournament = get_object_or_404(Tournament, title=tournament)

    try:
        tours_list = Tour.objects.filter(tournament=tournament)
        players_stat = PlayerStats.objects.filter(tournament=tournament)
    except Tour.DoesNotExist:
        pass
    except PlayerStats.DoesNotExist:
        pass

    context = {
        'tournament': tournament,
        'tours_list': tours_list,
        'players_stat': players_stat,
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
        matches = Match.objects.filter(tour=tour)
    except PlayerStats.DoesNotExist:
        pass
    except Match.DoesNotExist:
        pass

    context = {
        'tour': tour,
        'players_stat': players_stat,
        'matches': matches,
        }

    return render(request, 'tour_detail.html', context=context)


def match_detail_view(request, tournament, tour_pk, match_pk):
    '''
    Отображение детальной информации о матче.

    Attributes:
        match: Выбранный матч.
        tour: Используется для ссылки на тур.
        tournament: Используется для ссылки на турнир.
    '''
    match = get_object_or_404(Match.objects.select_related('tour'), id=match_pk)

    context = {
        'match': match,
        'tour': match.tour,
        'tournament': match.tour.tournament,
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
    return render(request, 'tournament_start_form.html', {'tournament': tournament, 'start_form': start_form, })
