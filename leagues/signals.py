from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=league)
def create_league_settings(sender,instance,created,**kwargs):
    if created:
        league_settings.objects.create(league_name=instance)

@receiver(post_save, sender=league)
def save_league_settings(sender, instance, **kwargs):
    instance.league_settings.save()