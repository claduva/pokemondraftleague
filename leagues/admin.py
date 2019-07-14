from django.contrib import admin

from .models import *


class LeagueAdmin(admin.ModelAdmin):
    model= league
    filter_horizontal = ('host',) #If you don't specify this, you will get a multiple select widget.

# Register your models here.
admin.site.register(league,LeagueAdmin)
admin.site.register(league_settings)
admin.site.register(league_application)
admin.site.register(coachdata)
admin.site.register(award)
admin.site.register(coachaward)
admin.site.register(leaguetiers)
admin.site.register(leaguetiertemplate)
admin.site.register(seasonsetting)
admin.site.register(roster)
admin.site.register(draft)
admin.site.register(discord_settings)
admin.site.register(draft_announcements)