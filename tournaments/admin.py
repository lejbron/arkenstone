from django.contrib import admin

from .models import Challenge, Match, Tour, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'superviser', 'start_date', 'start_time', 'tours_amount',
        'tt_status', 'tt_category', 'tt_type')
    list_filter = (
        'tt_status', 'tt_category', 'tt_type'
    )
    fieldsets = (
      ('Tournament info', {
          'fields': ('title', 'start_date', 'start_time', 'tours_amount')
      }),
      ('Management', {
          'fields': ('superviser', 'tt_category', 'tt_type')
      }),
      ('Administration', {
          'fields': ('tt_status', 'tt_slug')
      }),
    )


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('order_num', 'tour_status', 'tournament',)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'user', 'opponent',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tour', 'table', 'opp1', 'opp2', 'opp1_gp', 'opp2_gp')
