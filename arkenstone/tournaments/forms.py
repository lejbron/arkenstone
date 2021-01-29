from django import forms
from django.forms import inlineformset_factory

from .models import Match, PlayerStats, Tour, Tournament


class TournamentRegisterForm(forms.ModelForm):
    class Meta:
        model = PlayerStats
        fields = ('army',)


class TournamentStartForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('status',)


class TourResultsForm(forms.ModelForm):
    class Meta:
        model = Tour
        exclude = ()


MatchesPairsFormSet = inlineformset_factory(
    Tour,
    Match,
    form=TourResultsForm,
    fields=('opp1', 'opp2'),
    extra=0,
    can_delete=False,
)

MatchesResultsFormSet = inlineformset_factory(
    Tour,
    Match,
    form=TourResultsForm,
    fields=('opp1', 'opp2', 'opp1_gp', 'opp2_gp'),
    extra=0,
    can_delete=False,
    )
