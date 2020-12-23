from django.urls import path
from django.conf.urls import url
from .views import LeaderboardView

urlpatterns = [
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard_list'),
    ]
