from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/", views.league_list, name="league_list"),
    path("leagues/recruiting", views.recruiting_league_list, name="recruiting_league_list"),
    path("leagues/createleague/", views.create_league, name="create_league"),
    path("leagues/<str:league_name>/", views.league_detail, name="league_detail"),
    path("leagues/<str:league_name>/apply/", views.league_apply, name="league_application"),
    path("settings/league/", views.leagues_hosted_settings, name="leagues_hosted_settings"),
    path("settings/coaching/", views.leagues_coaching_settings, name="leagues_coaching_settings"),
    path("settings/coaching/<str:league_name>/", views.individual_league_coaching_settings, name="individual_league_coaching_settings"),
    path("settings/coaching/<str:league_name>/designatezusers/", views.designate_z_users, name="designate_z_users"),
    path("settings/league/<str:league_name>/", views.individual_league_settings, name="individual_league_settings"),
    path("settings/league/<str:league_name>/managecoachs/", views.manage_coachs, name="manage_coachs"),
    path("settings/league/<str:league_name>/managecoachs/addcoach/", views.add_coach, name="addcoach"),
    path("settings/league/<str:league_name>/managecoachs/removecoach/", views.remove_coach, name="removecoach"),
     path("settings/league/<str:league_name>/managecoachs/managecoach/", views.manage_coach, name="managecoach"),
    path("settings/league/<str:league_name>/managetiers/", views.manage_tiers, name="manage_tiers"),
    path("settings/league/<str:league_name>/managetiers/tier/<str:tier>/", views.view_tier, name="view_tier"),
    path("settings/league/<str:league_name>/managetiers/default/", views.default_tiers, name="default_tiers"),
    path("settings/league/<str:league_name>/updatetier/", views.update_tier, name="update_tier"),
    path("settings/league/<str:league_name>/managetiers/edittier/<int:tierid>/", views.edit_tier, name="edit_tier"),
    path("settings/league/<str:league_name>/managetiers/deletetier/", views.delete_tier, name="delete_tier"),
    path("settings/league/<str:league_name>/manageseasons/", views.manage_seasons, name="manage_seasons"),
    path("settings/league/<str:league_name>/manageseasons/setdraftorder", views.set_draft_order, name="set_draft_order"),
    path("settings/league/<str:league_name>/conferenceanddivisionnames", views.add_conference_and_division_names, name="add_conference_and_division_names"),
    path("settings/league/<str:league_name>/conferenceanddivisionnames/deleteconference", views.delete_conference, name="delete_conference"),
    path("settings/league/<str:league_name>/conferenceanddivisionnames/deletedivision", views.delete_conference, name="delete_division"),
    path("settings/league/<str:league_name>/deleteleague/", views.delete_league, name="delete_league"),
]