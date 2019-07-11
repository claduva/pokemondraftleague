from django.urls import path

from . import views

urlpatterns = [ 
    path("leagues/<str:league_name>/seasons/", views.otherseasonslist, name="otherseasonslist"),
    path("leagues/<str:league_name>/seasons/<str:seasonofinterest>/", views.seasondetail, name="seasondetail"),
    path("leagues/<str:league_name>/seasons/<str:seasonofinterest>/draft/", views.seasondraft, name="seasondraft"),
    path("leagues/<str:league_name>/seasons/<str:seasonofinterest>/transactions/", views.seasontransactions, name="seasontransactions"),
    path("leagues/<str:league_name>/seasons/<str:seasonofinterest>/<str:teamofinterest>/", views.seasonteamdetail, name="seasonteamdetail"),
]