from django.urls import path

from . import views

urlpatterns = [ 
    path("pokemon/", views.pokedex, name="pokedex"),
    path("pokemon/<str:pokemon_of_interest>/", views.pokedex_item, name="pokedex_item"),
]