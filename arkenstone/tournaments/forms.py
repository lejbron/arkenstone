from django import forms

from .models import Match, PlayerStats, Tournament


class TournamentRegisterForm(forms.ModelForm):
    class Meta:
        model = PlayerStats
        fields = ('army',)


class TournamentStartForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('status',)


class SetMatchPairsForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('opp1', 'opp2', )
