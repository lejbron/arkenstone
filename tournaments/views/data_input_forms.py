from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from players.models import PlayerStats
from tournaments.forms import (
    MatchesResultsFormSet, TournamentCreationForm, TournamentRegisterForm,
)
from tournaments.models import Tour, Tournament

User = get_user_model()


@login_required
def create_tournament(request):
    """
    View-функция формы создания турнира.

    Attributes:
        crt_form: Форма создания турнира.
    """
    data = request.POST or None
    crt_form = TournamentCreationForm(data)  # MyForm(data)
    if crt_form.is_valid():
        tournament = crt_form.save(commit=False)
        superviser_id = crt_form.cleaned_data['superviser_id']
        superviser = get_object_or_404(User, id=superviser_id)
        tournament.superviser = superviser
        tournament.save()
        return redirect('index')
    context = {
        'crt_form': crt_form,
    }
    return render(request, 'tournament_crt_form.html', context)


@login_required
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
    context = {
        'tournament': tournament,
        'reg_form': reg_form,
    }
    if not reg_form.is_valid() or tournament.superviser == request.user:
        return render(request, 'tournament_reg_form.html', context)
    player_stat = reg_form.save(commit=False)
    player_stat.tournament = tournament
    player_stat.player = request.user
    player_stat.save()
    return redirect('index')


@login_required
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
