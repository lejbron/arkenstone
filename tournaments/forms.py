from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from tempus_dominus.widgets import DatePicker, TimePicker

from .models import Match, PlayerStats, Tour, Tournament

User = get_user_model()


class TournamentCreationForm(forms.ModelForm):
    """
    Форма создания турнира.
    """
    superviser_id = forms.ChoiceField(
        label='Организатор',
        choices=User.objects.filter(is_staff=True).values_list('id', 'username'),
        )

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
                    'append': 'far fa-calendar-alt',
                    'icon_toggle': True,
                }
            ),
            'start_time': TimePicker(
                options={
                    'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
                    'defaultDate': '1992-01-01T10:00:00'
                },
                attrs={
                    'append': 'far fa-clock',
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
