from django.urls import path

from . import views

urlpatterns = [ 
    path("replayanalysis/", views.replay_analysis, name="replay_analysis"),
    path("leagues/<str:league_name>/<str:subleague_name>/uploadreplay/<int:matchid>", views.upload_league_replay, name="upload_league_replay"),
    path("leagues/<str:league_name>/<str:subleague_name>/matchresults/<int:matchid>/", views.league_match_results, name="league_match_results"),
    path("checkpasses/", views.check_if_passes, name="check_if_passes"),
    path("checkanalyzer/", views.check_analyzer, name="check_analyzer"),
    path("checkexistingreplay/", views.check_existing_replay, name="check_existing_replay"),
    path("upload_historic_match/", views.upload_historic_match, name="upload_historic_match"),
    path("uploadhistoricrender/", views.uploadhistoricrender, name="uploadhistoricrender"),
    path("renderreplay/<str:string>/", views.render_uploaded_replay, name="render_uploaded_replay"),
    path("checkanalyzer/currentmatch/", views.check_current_match, name="check_current_match"),
    path("checkanalyzer/histmatch/", views.check_hist_match, name="check_hist_match"),
]