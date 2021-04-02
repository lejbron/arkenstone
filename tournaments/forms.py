from django import forms
from django.forms import inlineformset_factory
from tempus_dominus.widgets import DatePicker, TimePicker

from .models import Match, PlayerStats, Tour, Tournament


class TournamentCreationForm(forms.ModelForm):
    """
    Форма создания турнира.
    """
    class Meta:
        model = Tournament
        fields = ('title', 'start_date', 'start_time', 'tours_amount', 'tt_category', 'tt_type')
        widgets = {
            'start_date': DatePicker(
                options={
                    'useCurrent': True,
                    'collapse': False,
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                }
            ),
            'start_time': TimePicker(
                options={
                    'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
                    'defaultDate': '1970-01-01T14:56:00'
                },
                attrs={
                    'append': 'fa fa-calendar',
                    'icon_toggle': True,
                },
            ),
        }


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
