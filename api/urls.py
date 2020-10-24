from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'overdue', views.OverdueViewSet,base_name='overdue')
router.register(r'schedule', views.ScheduleViewSet,base_name='schedule')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
]