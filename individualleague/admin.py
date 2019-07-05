from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(schedule)
admin.site.register(rule)
admin.site.register(free_agency)
admin.site.register(trading)
admin.site.register(trade_request)
admin.site.register(hall_of_fame_entry)
admin.site.register(hall_of_fame_roster)
admin.site.register(replay_announcements)
admin.site.register(trading_announcements)
admin.site.register(freeagency_announcements)
admin.site.register(pickems)