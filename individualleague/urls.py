from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/<str:league_name>/teams/<str:team_abbreviation>", views.team_page, name="team_page"),
    path("leagues/<str:league_name>/draft", views.league_draft, name="league_draft"),
]