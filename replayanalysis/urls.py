from django.urls import path

from . import views

urlpatterns = [ 
    path("replayanalysis/", views.replay_analysis, name="replay_analysis"),
]