from django import forms
from django.forms import inlineformset_factory

from .models import Match, PlayerStats, Tour, Tournament


class TournamentCreationForm(forms.ModelForm):
    """
    Форма создания турнира.
    """
    class Meta:
        model = Tournament
        fields = ('title', 'start_date', 'tours_amount', 'tt_category', 'tt_type')


class TournamentRegisterForm(forms.ModelForm):
    """
    Форма регистрации на турнир.
    """
    class Meta:
        model = PlayerStats
        fields = ('army',)


class TourResultsForm(forms.ModelForm):
    """
    Форма обновления результатов тура.
    """
    class Meta:
        model = Tour
        fields = ('tour_status', )
        exclude = ()


MatchesResultsFormSet = inlineformset_factory(
    Tour,
    Match,
    form=TourResultsForm,
    fields=('opp1', 'opp2', 'opp1_gp', 'opp2_gp'),
    extra=0,
    can_delete=False,
    )
