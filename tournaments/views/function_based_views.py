# from django.contrib.auth.models import User
# from django.forms import inlineformset_factory
import json

from django.shortcuts import get_object_or_404, render

from tournaments.forms import ProxyBotAddForm
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
    tournaments_reglist = request.user.tt_stats.all().values_list('tournament', flat=True)

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
    count = tournament.players.count()
    odd_number_flag = False
    if count % 2 != 0:
        odd_number_flag = True
    proxy_bot_form = ProxyBotAddForm(request.POST or None)
    context = {
        'tournament': tournament,
        'players_stat': tournament.players.all(),
        'odd_number_flag': odd_number_flag,
        'proxy_bot_form': proxy_bot_form,
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
