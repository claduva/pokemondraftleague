from django.urls import path

from . import views

urlpatterns = [ 
    path("settings/admin/", views.pokemonadminhome, name="pokemonadmin"),
    path("changehistoricattribution/<int:matchid>/", views.change_historic_match_attribution, name="change_historic_match_attribution"),
]