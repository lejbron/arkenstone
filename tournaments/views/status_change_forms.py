from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from tournaments.decorators import superviser_check
from tournaments.models import Tour, Tournament


@login_required
@superviser_check
def open_registration(request, tt_slug):
    """
    View-функция, открывающая регистрацию на турнир.
    Доступна только организаторам.

    Attributes:
        tournament: Выбранный турнир.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)
    tournament.tt_status = 'reg'
    tournament.save()
    return redirect('tournament-detail', tournament.tt_slug)


@login_required
@superviser_check
def close_registration(request, tt_slug):
    """
    View-функция, закрывающая регистрацию на турнир.
    Доступна только организаторам.

    Attributes:
        tournament: Выбранный турнир.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)
    count = tournament.players.count()
    if (count % 2 == 1) or (count == 0):
        return redirect('tournaments-list')
    tournament.tt_status = 'creg'
    tournament.save()
    return redirect('tournament-detail', tournament.tt_slug)


@login_required
@superviser_check
def start_tournament(request, tt_slug):
    """
    View-функция формы запуска турнира. Доступна только организаторам.

    Attributes:
        tournament: Выбранный турнир.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    tournament.tt_status = 'act'
    tournament.save()
    tournament.create_tours()
    return redirect('tournament-detail', tournament.tt_slug)


@login_required
@superviser_check
def start_tour(request, tour_slug):
    """
    View-функция формы запуска турнира. Доступна только организаторам.

    Attributes:
        tour: Выбранный тур.
    """
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    tour.tour_status = 'act'
    tour.save()
    tour.create_matches()
    return redirect('tour-detail', tour.tour_slug)


@login_required
@superviser_check
def finish_tour(request, tour_slug):
    """
    View-функция формы завершения турнира. Доступна только организаторам.

    Attributes:
        tour: Выбранный тур.
    """
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    tour.tour_status = 'fin'
    tour.update_tour_results()
    tour.save()
    if tour.order_num == tour.tournament.tours_amount:
        tour.tournament.finish_tournament()
    return redirect('tour-detail', tour.tour_slug)
