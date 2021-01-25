from django.contrib.auth.models import User
from django.contrib.postgres.validators import (MaxValueValidator,
                                                MinValueValidator)
from django.db import models

MAX_TOURS = 6


class Tournament(models.Model):
    """Model representing the Tournament."""

    TOURNAMENT_STATUSES = [
        ('ann', 'announce'),
        ('reg', 'registration'),
        ('creg', 'registration closed'),
        ('act', 'active'),
        ('fin', 'finished'),
    ]

    title = models.CharField(max_length=200)
    start_date = models.DateField(null=True)
    status = models.CharField(
        default='ann',
        max_length=4,
        choices=TOURNAMENT_STATUSES)
    tours_amount = models.PositiveIntegerField(
        default=3,
        blank=True,
        validators=[MinValueValidator(3), MaxValueValidator(MAX_TOURS)]
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title

#    def get_absolute_url(self):
#       """Returns the url to access a particular tournament instance."""
#        return reverse('tournament-detail', args=[str(self.id)])


class PlayerStats(models.Model):
    """Model representing player statistics for tournament."""

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        null=True)

    player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True)

    game_points = models.PositiveIntegerField(
        blank=True,
        default=None,
        null=True)
    tournament_points = models.PositiveIntegerField(
        blank=True,
        default=None,
        null=True)
    difference = models.IntegerField(
        blank=True,
        default=None,
        null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.player.username
