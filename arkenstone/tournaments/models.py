from django.contrib.auth.models import User
from django.contrib.postgres.validators import (MaxValueValidator,
                                                MinValueValidator)
from django.db import models
from django.urls import reverse

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

    title = models.CharField(
        max_length=200,
        unique=True)
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

    @property
    def registered_players(self):
        try:
            return PlayerStats.objects.filter(tournament=self)
        except PlayerStats.DoesNotExist:
            print('No players registered yet')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular tournament instance."""
        return reverse('tournament-detail', args=[str(self)])

    def create_tours(self):
        for i in range(1, self.tours_amount + 1):
            tour = Tour(
                tournament=self,
                order_num=i,
                tour_status='crt',
            )
            tour.save()
            tour.create_matches()


class PlayerStats(models.Model):
    """Model representing player statistics for tournament."""

    tournament = models.ForeignKey(
        Tournament,
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
                name='unique_tournament_paleyr',
                fields=['tournament', 'player'])
        ]

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
        limit_choices_to={'status__in': ['ann', 'reg', 'act']},
        related_name='tours')
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

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('tour-detail', args=[str(self.tournament), str(self.id)])

    def create_matches(self):
        try:
            players = PlayerStats.objects.filter(tournament=self.tournament)
            for i in range(0, self.tournament.registered_players.count(), 2):
                if self.order_num == 1:
                    m = Match(
                        tour=self,
                        opp1=players[i].player,
                        opp2=players[i+1].player,
                    )
                    m.save()
                else:
                    m = Match(
                        tour=self,
                    )
                    m.save()
        except PlayerStats.DoesNotExist:
            print('Create Match Stats error')


class Match(models.Model):
    """Model representing a match between opponents unique for tour."""
    MAX_GAME_POINTS = 12

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='matches')

    opp1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='opp1',)
    opp2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='opp2',)

    opp1_gp = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True,
        validators=[MaxValueValidator(MAX_GAME_POINTS)])

    opp2_gp = models.PositiveIntegerField(
        default=None,
        blank=True,
        null=True,
        validators=[MaxValueValidator(MAX_GAME_POINTS)])

    @property
    def opp1_army(self):
        try:
            return PlayerStats.objects.filter(tournament=self.tour.tournament).get(player=self.opp1).army
        except PlayerStats.DoesNotExist:
            print('Match property error')

    @property
    def opp2_army(self):
        try:
            return PlayerStats.objects.filter(tournament=self.tour.tournament).get(player=self.opp2).army
        except PlayerStats.DoesNotExist:
            print('Match property error')

    class Meta:
        verbose_name_plural = 'matches'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.opp1} vs {self.opp2}'

    def get_absolute_url(self):
        """Returns the url to access a particular match instance."""
        return reverse(
            'match-detail',
            args=[str(self.tour.tournament), str(self.tour.order_num), str(self.id)])
