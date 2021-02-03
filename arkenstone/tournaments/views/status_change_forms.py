from django.shortcuts import get_object_or_404, redirect

from ..models import Tour, Tournament


def start_tournament(request, tt_slug):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tournament = get_object_or_404(Tournament, tt_slug=tt_slug)

    tournament.status = 'act'
    tournament.save()
    tournament.create_tours()
    return redirect('tournament-detail', tournament.tt_slug)


def start_tour(request, tour_slug):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    tour.tour_status = 'act'
    tour.save()
    tour.create_matches()
    return redirect('tour-detail', tour.tour_slug)


def finish_tour(request, tour_slug):
    '''
    Форма запуска турнира. Доступна только организаторам.
    '''
    tour = get_object_or_404(Tour, tour_slug=tour_slug)

    tour.tour_status = 'fin'
    tour.update_tour_results()
    tour.save()
    return redirect('tour-detail', tour.tour_slug)
