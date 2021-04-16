import json
import random

from django.contrib.auth import get_user_model
from django.contrib.postgres.validators import (
    MaxValueValidator, MinValueValidator,
)
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from pytils.translit import slugify

from players.models import PlayerStats

MAX_TOURS = 6

User = get_user_model()


class Tournament(models.Model):
    """
    Турнир

    Attributes:
        supervizor: Организатор турнира.
                    owned_tournaments - Туринры, которые создавал организатор.
        title: Название турнира.
        strat_date: Дата начала турнира.
        tours_amout: Количество туров.
        tt_category: Категория турнира - нарративный или рейтинговый.
        tt_type: Тип турнира - соло, парный, командный.
        tt_status: Статус турнира, не доступен для ручного изменения.
        tt_slug: URL-постфикс страницы турнира.
    Properties:
        registered_palyers: Список зарегистрированных на турнир игроков.
    Methods:
        save: при создании турнира поле title преобразуется в slug и присваивается tt_slug.
        create_tours: создает указанное в tours_amount количество туров.
    """

    TOURNAMENT_STATUSES = [
        ('ann', 'Анонс'),
        ('reg', 'Регистрация открыта'),
        ('creg', 'Регистрация закрыта'),
        ('act', 'Активный'),
        ('fin', 'Завершен'),
    ]

    CATEGORIES = [
        ('nrt', 'Нарративный'),
        ('rtg', 'Рейтинговый'),
        ('nyt', 'Новогодний')
    ]

    TYPES = [
        ('s', 'Одиночный'),
        ('d', 'Парный'),
        ('t', 'Командный')
    ]
    superviser = models.ForeignKey(
        User,
        verbose_name='Организатор',
        help_text='Укажите организатора турнира',
        on_delete=models.SET_NULL,
        related_name='owned_tournaments',
        null=True,
    )
    title = models.CharField(
        verbose_name='Название',
        help_text='Название турнира',
        max_length=200,
        unique=True
    )
    start_date = models.DateField(
        verbose_name='Дата',
        help_text='Дата проведения турнира',
        default=timezone.now,
        null=True
    )
    start_time = models.TimeField(
        verbose_name='Время',
        help_text='Время проведения турнира',
        default=timezone.now
    )
    tours_amount = models.PositiveIntegerField(
        verbose_name='Кол-во туров',
        help_text=f'Укажите количество туров в турнире - от 3 до {MAX_TOURS}',
        default=3,
        validators=[MinValueValidator(3), MaxValueValidator(MAX_TOURS)]
    )
    tt_category = models.CharField(
        verbose_name='Категория',
        help_text='Выберите категорию турнира из списка',
        default='rtg',
        max_length=4,
        choices=CATEGORIES,
    )
    tt_type = models.CharField(
        verbose_name='Тип турнира',
        help_text='Выберите тип турнира из списка',
        default='s',
        max_length=4,
        choices=TYPES,
    )
    tt_status = models.CharField(
        verbose_name='Статус турнира',
        help_text='Укажите статус турнира',
        default='ann',
        max_length=4,
        choices=TOURNAMENT_STATUSES,
    )

    tt_slug = models.SlugField(
        verbose_name='Слаг турнира',
        help_text='Укажите слаг турнира',
        null=True,
        unique=True,
        blank=True,
    )

    @property
    def tours_str(self):
        if self.tours_amount in [3, 4]:
            tstr = f'{self.tours_amount} тура'
        elif self.tours_amount in [5, 6]:
            tstr = f'{self.tours_amount} туров'
        return tstr

    class Meta:
        ordering = [('-start_date'), ]

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def save(self, *args, **kwargs):
        """
        Attributes:
            tt_slug: Преобразованное название турнира.
        """
        if self.tt_slug is None:
            super(Tournament, self).save(*args, **kwargs)
            self.tt_slug = slugify(self)
        super(Tournament, self).save(*args, **kwargs)

    def is_registered(self, user):
        return user.tt_stats.filter(tournament=self).exists()

    def get_absolute_url(self):
        """Returns the url to access a particular tournament instance."""
        return reverse('tournament-detail', args=[self.tt_slug])

    def create_tours(self):
        """
        Функция создания указанного в tours_amount количества туров.
        """
        if self.tt_status == 'act':
            for i in range(1, self.tours_amount + 1):
                tour = Tour(
                    tournament=self,
                    order_num=i,
                    tour_status='crt',
                )
                tour.save()
        else:
            print('Tournament is not active!')

    def finish_tournament(self):
        """
        Функция завршения турнира.
        После завршения турнира данные о сыгранных матчах становятся недоступны для редактирования.
        """
        self.tt_status = 'fin'
        self.save()


class Tour(models.Model):
    """
    Тур

    Attributes:
        tournament: Турнир, в рамках которого создан тур.
        order_num: Порядковый номер тура.
        tour_status: Статус турнира.
        tour_slug: URL-постфикс страницы тура.
        tour_results: JSON с результатами турнира на момент завршения тура.

    Properties:
        all_results_ready: bool - внесены ли результаты всех матчей тура.
        previous_finished: bool - завершен ли предыдущий тур.

    Methods:
        save: при создании тура поле title преобразуется в slug и присваивается tt_slug.
        create_matches: создает матчи для тура.
        update_tour_results: обновляет промежуточные результаты турнира после завршения тура.
    """
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
        limit_choices_to={'tt_status__in': ['ann', 'reg', 'act']},
        related_name='tours'
    )
    order_num = models.PositiveIntegerField(
        default=1,
        choices=TOURS_NUM
    )
    tour_status = models.CharField(
        default='crt',
        max_length=4,
        choices=TOUR_STATUSES
    )
    tour_slug = models.SlugField(
        null=True,
        unique=True
    )
    tour_results = models.JSONField(
        null=True,
        blank=True
    )

    @property
    def all_results_ready(self) -> bool:
        return not Match.objects.filter(tour=self).filter(Q(opp1_gp__exact=None) | Q(opp2_gp__exact=None)).exists()

    @property
    def previous_finished(self) -> bool:
        if self.order_num != 1:
            status = Tour.objects.filter(tournament=self.tournament).get(order_num=self.order_num-1).tour_status
            if status != 'fin':
                return False
        return True

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_tour', fields=['order_num', 'tournament_id'])
        ]
        ordering = ['tournament', 'order_num']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.order_num} tour'

    def save(self, *args, **kwargs):
        """
        Attributes:
            slug_str: Преобразованное название турнира и № тура.
        """
        if self.tour_slug is None:
            super(Tour, self).save(*args, **kwargs)
            slug_str = str(self.tournament) + '-' + str(self)
            self.tour_slug = slugify(slug_str)
        super(Tour, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns the url to access a particular tour instance."""
        return reverse('tour-detail', args=[str(self.tour_slug)])

    def create_matches(self):
        """
        Создание матчей для тура.

        Attributes:
            players: Список зарегистриованных на турнир игроков.
        """
        players = list(self.tournament.players.all())
        if self.order_num == 1:
            random.shuffle(players)
        for i in range(0, len(players), 2):
            m = Match(
                tour=self,
                opp1=players[i],
                opp2=players[i+1],
            )
            m.save()

    def update_tour_results(self):
        """
        Обновление промежуточных результатов турнира на момент завершения тура.

        Attributes:
            json_data: Отсортированный по убыванию список результаов зарегистрированных на турнир игроков.
                       Порядок сортировки: турнирные очки, игровые очки, разница.
        """
        json_data = list(
            PlayerStats.objects.filter(tournament=self.tournament).
            values('player__id', 'player__username', 'game_points', 'difference', 'tournament_points'))
        self.tour_results = json.dumps(json_data)


class Match(models.Model):
    """
    Матч

    Attributes:
        tour: Тур, в рамках которого создан матч.
        table: Стол, на котором играется матч.
        opp1: Первый оппонент.
        opp2: Второй оппонент.
        opp1_gp: Игровые очки первого оппонента.
        opp2_gp: Игровые очки второго оппонента.
        match_slug: URL-постфикс страницы матча.

    Properties:
        opp1_tp: Турнирные очки первого оппонента.
        opp2_tp: Турнирные очки второго оппонента.
        opp1_diff: Разница игровых очков первого оппонента.
        opp2_diff: Разница игровых очков второго оппонента.

    Methods:
        save: при создании матча поле title преобразуется в slug и присваивается tt_slug.
        get_tournament_points: возвращает турнирые очки, заработанные в матче оппонентами.
        get_win_type: возвращает тип победы - минорная или большая.

    """
    MAX_GAME_POINTS = 12

    TP_POINTS = {
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

    table = models.PositiveIntegerField(
        default=666
    )

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
        """
        Attributes:
            slug_str: Преобразованное название турнира, № тура и ID матча.
        """
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
        """
        Возвращает рассчитанные по игровым очкам турнирные очки оппонентов.

        Attributes:
            tp1: Турнирные очки первого оппонента.
            tp2: Турнирные очки второго оппонента.
            win_type: Тип победы - minor/big.
        """
        if self.opp1_gp == self.opp2_gp:
            res1 = res2 = 'draw'
        elif self.opp1_gp > self.opp2_gp:
            win_type = self.get_win_type(self.opp1_gp, self.opp2_gp)
            res1 = win_type + 'Win'
            res2 = win_type + 'Loose'
        else:
            win_type = self.get_win_type(self.opp2_gp, self.opp1_gp)
            res2 = win_type + 'Win'
            res1 = win_type + 'Loose'

        tp1 = self.TP_POINTS[res1]
        tp2 = self.TP_POINTS[res2]

        return tp1, tp2

    def get_win_type(self, winner_gp, looser_gp):
        """
        Определние типа победы - minor/big.
        """
        if looser_gp == 0:
            if winner_gp == 1:
                return 'minor'
            else:
                return 'big'
        elif winner_gp >= looser_gp * 2:
            return 'big'
        else:
            return 'minor'
