from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('users/<str:username>/',views.user_profile,name="user_profile"),
    path('addfavorite/',views.favoritematch,name="favoritematch"),
    path('removefavorite/',views.unfavoritematch,name="unfavoritematch"),
    path('inbox/', views.inbox_view, name='inbox'),
    path('inbox/compose/', views.compose_message, name='compose'),
    path('inbox/delete/', views.delete_inbox, name='delete_inbox'),
    path('inbox/read/', views.read_inbox, name='read_inbox'),
    path('inbox/<int:messageid>/', views.inbox_item_view, name='inbox_item'),
    path('inbox/<int:messageid>/reply/', views.reply_message, name='reply'),
    path('inbox/<int:messageid>/delete/', views.inbox_item_delete, name='delete_inbox_item'),
    path('settings/user/',views.settings,name="settings"),
    path('settings/user/addalt',views.add_showdown_alt,name="addalt"),
    path('settings/site/',views.site_settings,name="site_settings"),
]