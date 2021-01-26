from django.contrib import admin

from .models import Match, PlayerStats, Tour, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'status', 'tours_amount',)


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ('player', 'tournament', 'army', 'game_points', 'tournament_points', 'difference',)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('order_num', 'tour_status', 'tournament',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour', 'opp1', 'opp2', 'opp1_gp', 'opp2_gp')
