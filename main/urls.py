from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("discordbot/", views.discordbotpage, name="discordbot"),
    path("pokemonleaderboard/", views.pokemonleaderboard, name="pokemonleaderboard"),
    path("userleaderboard/", views.userleaderboard, name="userleaderboard"),
    path("pickemleaderboard/", views.pickemleaderboard, name="pickemleaderboard"),
    path("replay_database/", views.replay_database, name="replay_database"),
    path("help/", views.help, name="help"),
    path("runscript/", views.runscript, name="runscript"),
]