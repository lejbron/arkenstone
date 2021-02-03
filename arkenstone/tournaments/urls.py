from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('<slug:tt_slug>/', views.tournament_detail_view, name='tournament-detail'),
    path('tours/<slug:tour_slug>/', views.tour_detail_view, name='tour-detail'),
    path('matches/<slug:match_slug>', views.match_detail_view, name='match-detail'),
]

urlpatterns += [
    path('<slug:tt_slug>/register/', views.register_on_tournament, name='tournament-reg'),
    path('<slug:tt_slug>/start/', views.start_tournament, name='tournament-start'),
]

urlpatterns += [
    path('tours/<slug:tour_slug>/start/', views.start_tour, name='tour-start'),
    path('tours/<slug:tour_slug>/pairs/', views.input_tour_pairs, name='tour-pairs'),
    path('tours/<slug:tour_slug>/results/', views.input_tour_results, name='tour-results'),
]
