from django.urls import path

from . import views

urlpatterns = [
    path('', views.tournaments_list_view, name='tournaments-list'),
    path('<int:pk>/', views.tournament_detail_view, name='tournament-detail'),
    path('<int:pk>/register/', views.register_on_tournament, name='tournament-reg'),
    path('tour/<int:pk>/', views.tour_detail_view, name='tour-detail'),
]
