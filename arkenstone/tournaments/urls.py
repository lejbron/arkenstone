from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('<str:tournament>/', views.tournament_detail_view, name='tournament-detail'),
    path('<str:tournament>/register/', views.register_on_tournament, name='tournament-reg'),
    path('<str:tournament>/tour/<int:tour_pk>/', views.tour_detail_view, name='tour-detail'),
]
