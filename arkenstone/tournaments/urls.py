from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('<str:tournament>/', views.tournament_detail_view, name='tournament-detail'),
    path('<str:tournament>/tour/<int:tour_pk>/', views.tour_detail_view, name='tour-detail'),
    path('<str:tournament>/tour/<int:tour_pk>/match/<int:match_pk>',
         views.match_detail_view, name='match-detail'),
]

urlpatterns += [
    path('<str:tt_title>/register/', views.register_on_tournament, name='tournament-reg'),
    path('<str:tt_title>/start/', views.start_tournament, name='tournament-start'),
    path('<int:tour_id>/pairs/', views.input_tour_pairs, name='tour-pairs'),
    path('<int:tour_id>/results/', views.input_tour_results, name='tour-results'),
]
