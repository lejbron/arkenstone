import json

from django.contrib.auth.models import User
from django.contrib.postgres.validators import (MaxValueValidator,
                                                MinValueValidator)
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse

# from django.core import serializers


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

    tt_slug = models.SlugField(
        null=True,
        unique=True,
        blank=True
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

    def save(self, *args, **kwargs):
        if self.tt_slug is None:
            super(Tournament, self).save(*args, **kwargs)
            self.tt_slug = slugify(self)
        super(Tournament, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a particular tournament instance."""
        return reverse('tournament-detail', args=[self.tt_slug])

    def create_tours(self):
        if self.status == 'act':
            for i in range(1, self.tours_amount + 1):
                tour = Tour(
                    tournament=self,
                    order_num=i,
                    tour_status='crt',
                )
                tour.save()
                if tour.order_num == 1:
                    tour.create_matches()
        else:
            print('Tournament is not active!')


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

    def update_player_stats(self):
        self.game_points = 0
        self.tournament_points = 0
        self.difference = 0
        player_matches = Match.objects.\
            filter(tour__tournament=self.tournament).\
            filter(Q(opp1__exact=self) | Q(opp2__exact=self))
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

    tour_results = models.JSONField(
        null=True,
        blank=True)

    tour_slug = models.SlugField(
        null=True,
        unique=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_tour', fields=['order_num', 'tournament_id'])
        ]
        ordering = ['tournament', 'order_num']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.order_num} tour'

    def save(self, *args, **kwargs):
        if self.tour_slug is None:
            super(Tour, self).save(*args, **kwargs)
            slug_str = str(self.tournament) + '-' + str(self)
            self.tour_slug = slugify(slug_str)
        super(Tour, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('tour-detail', args=[str(self.tour_slug)])

    def create_matches(self):
        players = self.tournament.registered_players
        for i in range(0, players.count(), 2):
            m = Match(
                tour=self,
                opp1=players[i],
                opp2=players[i+1],
            )
            m.save()

    def update_tour_results(self):
        json_data = list(
            PlayerStats.objects.filter(tournament=self.tournament).
            values('player__id', 'player__username', 'game_points', 'difference', 'tournament_points'))
        self.tour_results = json.dumps(json_data)
        self.save()


class Match(models.Model):
    """Model representing a match between opponents unique for tour."""
    MAX_GAME_POINTS = 12

    t_points_lookup = {
        'bigWin': 6,
        'minorWin': 5,
        'draw': 2,
        'minorLoose': 1,
        'bigLoose': 0
    }

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name='matches')

    opp1 = models.ForeignKey(
        PlayerStats,
        on_delete=models.SET_NULL,
        null=True,
        related_name='opp1',)
    opp2 = models.ForeignKey(
        PlayerStats,
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

    match_slug = models.SlugField(
        null=True,
        unique=True
    )

    @property
    def opp1_tp(self):
        if self.opp1_gp is not None:
            return self.get_tournament_points()[0]

    @property
    def opp2_tp(self):
        if self.opp2_gp is not None:
            return self.get_tournament_points()[1]

    @property
    def opp1_diff(self):
        if self.opp1_gp is not None and self.opp2_gp is not None:
            diff = self.opp1_gp - self.opp2_gp
            return diff

    @property
    def opp2_diff(self):
        if self.opp1_gp is not None and self.opp2_gp is not None:
            diff = self.opp2_gp - self.opp1_gp
            return diff

    class Meta:
        verbose_name_plural = 'matches'

    def save(self, *args, **kwargs):
        if self.match_slug is None:
            super(Match, self).save(*args, **kwargs)
            slug_str = str(self.tour.tournament) + '-' + str(self.tour) + '-' + str(self.id)
            self.match_slug = slugify(slug_str)
        super(Match, self).save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.opp1} vs {self.opp2}'

    def get_absolute_url(self):
        """Returns the url to access a particular match instance."""
        return reverse('match-detail', args=[str(self.match_slug)])

    def get_tournament_points(self):
        '''
        Возвращает рассчитанные по игровым очкам турнирные очки оппонентов.

        Attributes:
            tp1: Турнирные очки первого оппонента.
            tp2: Турнирные очки второго оппонента.
        '''
        if self.opp1_gp > self.opp2_gp:
            if self.opp1_diff >= self.opp2_gp:
                tp1 = self.t_points_lookup.get('bigWin')
                tp2 = self.t_points_lookup.get('bigLoose')
            else:
                tp1 = self.t_points_lookup.get('minorWin')
                tp2 = self.t_points_lookup.get('minorLoose')
        elif self.opp1_gp < self.opp2_gp:
            if self.opp2_diff >= self.opp1_gp:
                tp2 = self.t_points_lookup.get('bigWin')
                tp1 = self.t_points_lookup.get('bigLoose')
            else:
                tp2 = self.t_points_lookup.get('minorWin')
                tp1 = self.t_points_lookup.get('minorLoose')
        elif self.opp1_gp == self.opp2_gp:
            tp1 = tp2 = self.t_points_lookup.get('draw')

        return tp1, tp2
