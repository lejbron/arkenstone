from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from tournaments.models import PlayerStats


def player_detail_view(request, pk):
    """Функция отображения детальной информации об игроке."""
    player = get_object_or_404(User.objects.select_related('profile'), id=pk)

    armies = PlayerStats.objects.filter(player__exact=player)

    context = {
        'player': player,
        'armies': armies,
        }

    return render(request, 'player_detail.html', context=context)


def players_list_view(request):
    """Функция отображения списка игроков."""
    players_list = User.objects.all().select_related('profile')

    context = {'players_list': players_list, }

    return render(request, 'players_list.html', context=context)
