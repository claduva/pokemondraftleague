from django.urls import path

from . import views

urlpatterns = [ 
    path("replayanalysis/", views.replay_analysis, name="replay_analysis"),
    path("leagues/<str:league_name>/<str:subleague_name>/uploadreplay/<int:matchid>", views.upload_league_replay, name="upload_league_replay"),
    path("leagues/<str:league_name>/<str:subleague_name>/uploadreplay/<int:matchid>/manual/", views.upload_league_replay_manual, name="upload_league_replay_manual"),
    path("leagues/<str:league_name>/<str:subleague_name>/matchresults/<int:matchid>/", views.league_match_results, name="league_match_results"),
    path("checkanalyzer/", views.check_analyzer, name="check_analyzer"),
    path("checkanalyzer/currentmatch/", views.check_current_match, name="check_current_match"),
    path("checkanalyzer/histmatch/", views.check_hist_match, name="check_hist_match"),
]