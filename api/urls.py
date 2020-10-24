from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'overdue', views.OverdueViewSet,basename='overdue')
router.register(r'schedule', views.ScheduleViewSet,basename='schedule')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
]