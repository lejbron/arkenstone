from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('create/', views.create_tournament, name='tournament-crt'),
    path('<slug:tt_slug>/', views.tournament_detail_view, name='tournament-detail'),
    path('tours/<slug:tour_slug>/', views.tour_detail_view, name='tour-detail'),
    path('matches/<slug:match_slug>', views.match_detail_view, name='match-detail'),
]

urlpatterns += [
    path('<slug:tt_slug>/register/', views.register_on_tournament, name='tournament-reg'),
    path('<slug:tt_slug>/start/', views.start_tournament, name='tournament-start'),
    path('<slug:tt_slug>/open-registration/', views.open_registration, name='tournament-open-reg'),
    path('<slug:tt_slug>/close-registration/', views.close_registration, name='tournament-close-reg'),
]

urlpatterns += [
    path('tours/<slug:tour_slug>/start/', views.start_tour, name='tour-start'),
    path('tours/<slug:tour_slug>/results/', views.input_tour_results, name='tour-results'),
    path('tours/<slug:tour_slug>/finish/', views.finish_tour, name='tour-finish'),
]

urlpatterns += [
    path('<slug:tt_slug>/<int:player_id>/create-challenge', views.challenge_create, name='challenge_create'),
    path('<slug:tt_slug>/<int:player_id>/cancel-challenge', views.challenge_cancel, name='challenge_cancel'),
    path('<slug:tt_slug>/<int:player_id>/accept-challenge', views.challenge_accept, name='challenge_accept'),
    path('<slug:tt_slug>/<int:player_id>/refuse-challenge', views.challenge_refuse, name='challenge_refuse'),
]
