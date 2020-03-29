from django.urls import path

from . import views

urlpatterns = [ 
    path("draftplanner/", views.draftplanner, name="draftplanner"),
    path("draftplanner/getdraft", views.getdraft, name="getdraft"),
    path("draftplanner/gettiers", views.gettiers, name="gettiers"),
    path("draftplanner/savedraft", views.savedraft, name="savedraft"),
    path("draftplanner/deletedraft", views.deletedraft, name="deletedraft"),
]