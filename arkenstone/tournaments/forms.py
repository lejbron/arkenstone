from django import forms

from .models import PlayerStats


class TournamentRegisterForm(forms.ModelForm):
    class Meta:
        model = PlayerStats
        fields = ('army',)
