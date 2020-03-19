from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/<str:league_name>/", views.league_detail, name="league_detail"),
    path("leagues/<str:league_name>/apply/", views.league_apply, name="league_application"),
    path("leagues/<str:league_name>/teampage/<str:team_name>/", views.teampage_detail, name="teampage_detail"),
    path("leagues/<str:league_name>/schedule/", views.total_league_schedule, name="total_league_schedule"),
    path("leagues/<str:league_name>/playoffs/", views.total_league_playoffs, name="total_league_playoffs"),
    path("leagues/<str:league_name>/league_leaders/", views.composite_league_leaders, name="composite_league_leaders"),
    path("leagues/<str:league_name>/schedule/<str:week>/<str:teamname>/", views.composite_weekly_matchup, name="composite_weekly_matchup"),
    path("leagues/<str:league_name>/<str:subleague_name>/", views.subleague_detail, name="subleague_detail"),
    path("leagues/<str:league_name>/<str:subleague_name>/teams/<str:team_abbreviation>/", views.team_page, name="team_page"),
    path("leagues/<str:league_name>/<str:subleague_name>/draft/", views.league_draft, name="league_draft"),
    path("leagues/<str:league_name>/<str:subleague_name>/free-agency/", views.freeagency, name="free_agency"),
    path("leagues/<str:league_name>/<str:subleague_name>/trading/", views.trading_view, name="trading"),
    path("leagues/<str:league_name>/<str:subleague_name>/schedule/", views.league_schedule, name="league_schedule"),
    path("leagues/<str:league_name>/<str:subleague_name>/matchup/<int:matchid>", views.league_matchup, name="league_matchup"),
    path("changeattribution/<int:matchid>/", views.change_match_attribution, name="change_match_attribution"),
    path("leagues/<str:league_name>/<str:subleague_name>/rules/", views.league_rules, name="league_rules"),
    path("leagues/<str:league_name>/<str:subleague_name>/rules/edit", views.edit_league_rules, name="edit_league_rules"),
    path("leagues/<str:league_name>/<str:subleague_name>/tiers/", views.league_tiers, name="league_tiers"),
    path("leagues/<str:league_name>/<str:subleague_name>/league_leaders/", views.league_leaders, name="league_leaders"),
    path("leagues/<str:league_name>/<str:subleague_name>/hall_of_fame/", views.league_hall_of_fame, name="league_hall_of_fame"),
    path("leagues/<str:league_name>/<str:subleague_name>/playoffs/", views.league_playoffs, name="league_playoffs"),
    path('pokemon-autocomplete/',views.PokemonAutocomplete.as_view(),name='pokemon-autocomplete',),
]