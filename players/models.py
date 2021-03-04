from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.shortcuts import get_list_or_404


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)


class PlayerStats(models.Model):
    """Model representing player statistics for tournament."""

    tournament = models.ForeignKey(
        'tournaments.Tournament',
        on_delete=models.CASCADE,
        null=True,)

    player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,)

    army = models.CharField(
        max_length=80,
        default='Shier')

    game_points = models.PositiveIntegerField(
        blank=True,
        default=0,
        null=True)
    tournament_points = models.PositiveIntegerField(
        blank=True,
        default=0,
        null=True)
    difference = models.IntegerField(
        blank=True,
        default=0,
        null=True)

    class Meta:
        verbose_name_plural = 'Players Stats'
        ordering = ['-tournament_points', '-difference', '-game_points']
        constraints = [
            models.UniqueConstraint(
                name='unique_tournament_player',
                fields=['tournament', 'player'])
        ]

    def __str__(self):
        """String for representing the Model object."""
        return self.player.username

    def update_player_stats(self):
        self.game_points = 0
        self.tournament_points = 0
        self.difference = 0

        player_matches = get_list_or_404(
            apps.get_model('tournaments.Match'),
            Q(opp1__exact=self) | Q(opp2__exact=self),
            tour__tournament=self.tournament,
        )
        for m in player_matches:
            if m.opp1 == self and m.opp1_gp is not None:
                self.game_points += m.opp1_gp
                self.tournament_points += m.opp1_tp
                self.difference += m.opp1_diff
            elif m.opp2_gp is not None:
                self.game_points += m.opp2_gp
                self.tournament_points += m.opp2_tp
                self.difference += m.opp2_diff
        self.save()
