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
        null=True,
        related_name='tournaments')

    player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True)

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

    def __str__(self):
        """String for representing the Model object."""
        return self.player.username


class Tour(models.Model):
    """Model representing one of tournament tours"""
    TOURS_NUM = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
    ]
    TOUR_STATUSES = [
        ('crt', 'created'),
        ('prd', 'paired'),
        ('act', 'active'),
        ('fin', 'finished'),
        ('arch', 'archived'),
    ]

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        limit_choices_to={'status__in': ['ann', 'reg', 'act']})
    order_num = models.PositiveIntegerField(
        default=1,
        choices=TOURS_NUM)
    tour_status = models.CharField(
        default='crt',
        max_length=4,
        choices=TOUR_STATUSES)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_tour', fields=['order_num', 'tournament_id'])
        ]

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.order_num} tour'

#    def get_absolute_url(self):
#        """Returns the url to access a particular tour instance."""
#        return reverse('tour-detail', args=[str(self.id)])
