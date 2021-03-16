# from django.contrib.auth.models import User
# from django.forms import inlineformset_factory
import json

from django.shortcuts import get_object_or_404, render

from players.models import PlayerStats
from tournaments.models import Match, Tour, Tournament


def tournaments_list_view(request):
    """
    View-функция отображения списка турниров.

    Attributes:
        tournaments_list: Список турниров. Статусы турнира: ['ann', 'reg', 'creg', 'act'].
        tournaments_reglist: Список значений id туриниров, на которые зараегистрирован
                             залогиненый пользователь. Необходим для определения кнопки
                             Зарегистрироваться/Покинуть.

    """
    tournaments_list = Tournament.objects.all()
    tournaments_reglist = []

    if not request.user.is_anonymous:
        players = PlayerStats.objects.filter(player=request.user)
        tournaments_reglist = players.values_list('tournament', flat=True)

    context = {
        'tournaments_list': tournaments_list,
        'tournaments_reglist': tournaments_reglist,
        }

    return render(request, 'tournaments_list.html', context=context)


def tournament_detail_view(request, tt_slug):
    """
    View-функция отображения детальной информации о турнире.

    Attributes:
        tournament: Выбранный турнир.
        players_stat: Текущие результаты турнира. Статусы турнира: ['act', 'fin'].
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    context = {
        'tournament': tournament,
        'players_stat': tournament.registered_players,
        }

    return render(request, 'tournament_detail.html', context=context)


def tour_detail_view(request, tour_slug):
    """
    View-функция отображения детальной информации о туре.

    Attributes:
        tour: Выбранный тур.
        json_stat: Промежуточные реузльтаты турнира. Доступны только после завршения тура.
    """
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    try:
        json_stat = json.loads(tour.tour_results)
    except TypeError:
        print('No results yet')
        json_stat = None

    context = {
        'tour': tour,
        'json_stat': json_stat,
        }

    return render(request, 'tour_detail.html', context=context)


def match_detail_view(request, match_slug):
    """
    View-функция отображения детальной информации о матче.

    Attributes:
        match: Выбранный матч.
    """
    match = get_object_or_404(Match, match_slug=match_slug)

    context = {
        'match': match,
        }

    return render(request, 'match_detail.html', context=context)
