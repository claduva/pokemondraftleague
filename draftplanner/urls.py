from django.urls import path

from . import views

urlpatterns = [ 
    path("draftplanner/", views.draftplanner, name="draftplanner"),
    path("draftplanner/getmon", views.getmon, name="getmon"),
    path("draftplanner/getdraft", views.getdraft, name="getdraft"),
    path("draftplanner/savedraft", views.savedraft, name="savedraft"),
    path("draftplanner/deletedraft", views.deletedraft, name="deletedraft"),
]