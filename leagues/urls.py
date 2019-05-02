from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/", views.league_list, name="league_list"),
    path("leagues/createleague/", views.create_league, name="create_league"),
    path("leagues/<str:league_name>/", views.league_detail, name="league_detail"),
    path("leagues/<str:league_name>/apply/", views.league_apply, name="league_application"),
    path("settings/league/", views.leagues_hosted_settings, name="leagues_hosted_settings"),
    path("settings/league/<str:league_name>/", views.individual_league_settings, name="individual_league_settings"),
    path("settings/league/<str:league_name>/managecoachs", views.manage_coachs, name="manage_coachs"),
    path("settings/league/<str:league_name>/managecoachs/addcoach", views.add_coach, name="addcoach"),
    path("settings/league/<str:league_name>/managecoachs/removecoach", views.remove_coach, name="removecoach"),
    path("settings/league/<str:league_name>/deleteleague", views.delete_league, name="delete_league"),
]