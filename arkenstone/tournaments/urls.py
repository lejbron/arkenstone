from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('<slug:tt_slug>/', views.tournament_detail_view, name='tournament-detail'),
    path('tours/<slug:tour_slug>/', views.tour_detail_view, name='tour-detail'),
    path('matches/<slug:match_slug>', views.match_detail_view, name='match-detail'),
]

urlpatterns += [
    path('<str:tt_title>/register/', views.register_on_tournament, name='tournament-reg'),
    path('<str:tt_title>/start/', views.start_tournament, name='tournament-start'),
    path('<int:tour_id>/pairs/', views.input_tour_pairs, name='tour-pairs'),
    path('<int:tour_id>/results/', views.input_tour_results, name='tour-results'),
]
