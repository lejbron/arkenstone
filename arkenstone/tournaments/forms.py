from django import forms

from .models import PlayerStats, Tournament


class TournamentRegisterForm(forms.ModelForm):
    class Meta:
        model = PlayerStats
        fields = ('army',)


class TournamentStartForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('status',)
