from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/<str:league_name>/teams/<str:team_abbreviation>/", views.team_page, name="team_page"),
    path("leagues/<str:league_name>/draft/", views.league_draft, name="league_draft"),
    path("leagues/<str:league_name>/free-agency/", views.freeagency, name="free_agency"),
    path("leagues/<str:league_name>/trading/", views.trading_view, name="trading"),
    path("leagues/<str:league_name>/schedule/", views.league_schedule, name="league_schedule"),
    path("leagues/<str:league_name>/matchup/<int:matchid>", views.league_matchup, name="league_matchup"),
    path("leagues/<str:league_name>/rules/", views.league_rules, name="league_rules"),
    path("leagues/<str:league_name>/rules/edit", views.edit_league_rules, name="edit_league_rules"),
    path("leagues/<str:league_name>/tiers/", views.league_tiers, name="league_tiers"),
    path("leagues/<str:league_name>/tiers-available/", views.available_league_tiers, name="available_league_tiers"),
    path("leagues/<str:league_name>/tiers/<str:tiername>/", views.individual_league_tier, name="individual_league_tier"),
    path("leagues/<str:league_name>/tiers-available/<str:tiername>/", views.available_individual_league_tier, name="available_individual_league_tier"),
    path("leagues/<str:league_name>/league_leaders/", views.league_leaders, name="league_leaders"),
    path("settings/league/<str:league_name>/manageseasons/creatematch/", views.create_match, name="create_match"),
    path("leagues/<str:league_name>/hall_of_fame/", views.league_hall_of_fame, name="league_hall_of_fame"),
    path("leagues/<str:league_name>/hall_of_fame/add_entry/", views.league_hall_of_fame_add_entry, name="league_hall_of_fame_add_entry"),
    path("leagues/<str:league_name>/hall_of_fame/add_roster/", views.league_hall_of_fame_add_roster, name="league_hall_of_fame_add_roster"),
    path('pokemon-autocomplete/',views.PokemonAutocomplete.as_view(),name='pokemon-autocomplete',),
]