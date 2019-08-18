from django.urls import path

from . import views

urlpatterns = [ 
    path("draftplanner/", views.draftplanner, name="draftplanner"),
]