from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("discorbot/", views.discordbotpage, name="discordbot"),
    path("pokemonleaderboard/", views.pokemonleaderboard, name="pokemonleaderboard"),
    path("userleaderboard/", views.userleaderboard, name="userleaderboard"),
    path("pickemleaderboard/", views.pickemleaderboard, name="pickemleaderboard"),
    path("runscript/", views.runscript, name="runscript"),
    path("updatematches/", views.updatematches, name="updatematches"),
    path("zerorosters/", views.zerorosters, name="zerorosters"),
]