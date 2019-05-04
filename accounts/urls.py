from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/',views.profile,name="profile"),
    path('settings/user/',views.settings,name="settings"),
    path('settings/user/addalt',views.add_showdown_alt,name="addalt"),
    path('settings/site/',views.site_settings,name="site_settings"),
]