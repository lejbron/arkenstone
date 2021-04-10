from django.shortcuts import get_object_or_404, redirect

from tournaments.models import Tour, Tournament


def start_tournament(request, tt_slug):
    """
    View-функция формы запуска турнира. Доступна только организаторам.

    Attributes:
        tournament: Выбранный турнир.
    """
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    tournament.create_tours()
    tournament.tt_status = 'act'
    tournament.save()

    return redirect('tournament-detail', tournament.tt_slug)


def start_tour(request, tour_slug):
    """
    View-функция формы запуска турнира. Доступна только организаторам.

    Attributes:
        tour: Выбранный тур.
    """
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    tour.create_matches()
    tour.tour_status = 'act'
    tour.save()
    return redirect('tour-detail', tour.tour_slug)


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
