from django.urls import path

from . import views

urlpatterns = [ 
    path("replayanalysis/", views.replay_analysis, name="replay_analysis"),
    path("leagues/<str:league_name>/uploadreplay/<int:matchid>", views.upload_league_replay, name="upload_league_replay"),
    path("leagues/<str:league_name>/uploadreplay/<int:matchid>/confirm/", views.confirm_league_replay, name="confirm_league_replay"),
    path("leagues/<str:league_name>/matchresults/<int:matchid>/", views.league_match_results, name="league_match_results"),
]