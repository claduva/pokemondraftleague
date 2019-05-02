from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(league)
admin.site.register(league_settings)
admin.site.register(league_application)
admin.site.register(coachdata)
admin.site.register(award)
admin.site.register(coachaward)