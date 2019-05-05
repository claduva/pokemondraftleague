from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/<str:league_name>/<str:team_abbreviation>", views.team_page, name="team_page"),
]