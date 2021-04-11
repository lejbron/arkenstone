from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Tournament


def superviser_check(func):
    """Декоратор. Проверяет является ли юзер организатором турнира."""
    @wraps(func)
    def wrap(request, *args, **kwargs):
        if kwargs.get('tt_slug'):
            tournament = get_object_or_404(Tournament, tt_slug=kwargs.get('tt_slug'))
        elif kwargs.get('tour_slug'):
            tournament = get_object_or_404(Tournament, tours__tour_slug=kwargs.get('tour_slug'))
        else:
            return func(request, *args, **kwargs)
        if tournament.superviser != request.user:
            raise PermissionDenied
        return func(request, *args, **kwargs)
    return wrap
