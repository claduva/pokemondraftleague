"""pokemondraft league website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('accounts.urls')),
    path('', include('draftplanner.urls')),
    path('', include('pokemonadmin.urls')),
    path('',include("otherseasons.urls")),
    path('',include("leagues.urls")),
    path('',include("individualleague.urls")),
    path('',include("main.urls")),
    path('',include("replayanalysis.urls")),
    path('',include("otherseasons.urls")),
    path('',include("pokemondatabase.urls")),
    url(r'^select2/', include('django_select2.urls')),
]

"""
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
"""

handler404 = 'main.views.custom404'
handler500 = 'main.views.custom500'
