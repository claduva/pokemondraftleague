from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(historical_draft)
admin.site.register(historical_roster)
admin.site.register(historical_freeagency)
admin.site.register(historical_trading)
admin.site.register(historical_match)
admin.site.register(historical_team)

