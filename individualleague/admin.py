from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(schedule)
admin.site.register(rule)
admin.site.register(free_agency)
admin.site.register(trading)
admin.site.register(trade_request)