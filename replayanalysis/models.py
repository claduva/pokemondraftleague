from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from django.contrib.postgres.fields import JSONField

from enum import Enum

from leagues.models import *
from individualleague.models import *

class manual_replay(models.Model):
    match=models.OneToOneField(schedule,on_delete=models.CASCADE)
    replay=models.CharField(max_length=200,default="None")
    t1megaevolved=models.BooleanField(default="False")
    t2megaevolved=models.BooleanField(default="False")
    t1usedz=models.BooleanField(default="False")
    t2usedz=models.BooleanField(default="False")
    t1pokemon1=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon1')
    t1pokemon2=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon2')
    t1pokemon3=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon3')
    t1pokemon4=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon4')
    t1pokemon5=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon5')
    t1pokemon6=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team1Pokemon6')
    t2pokemon1=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon1')
    t2pokemon2=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon2')
    t2pokemon3=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon3')
    t2pokemon4=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon4')
    t2pokemon5=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon5')
    t2pokemon6=models.ForeignKey(all_pokemon,on_delete=models.CASCADE, related_name='Team2Pokemon6')
    t1pokemon1kills=models.IntegerField(default=0)
    t1pokemon2kills=models.IntegerField(default=0)
    t1pokemon2kills=models.IntegerField(default=0)
    t1pokemon3kills=models.IntegerField(default=0)
    t1pokemon4kills=models.IntegerField(default=0)
    t1pokemon5kills=models.IntegerField(default=0)
    t1pokemon6kills=models.IntegerField(default=0)
    t2pokemon1kills=models.IntegerField(default=0)
    t2pokemon2kills=models.IntegerField(default=0)
    t2pokemon3kills=models.IntegerField(default=0)
    t2pokemon4kills=models.IntegerField(default=0)
    t2pokemon5kills=models.IntegerField(default=0)
    t2pokemon6kills=models.IntegerField(default=0)
    t1pokemon1death=models.IntegerField(default=0)
    t1pokemon2death=models.IntegerField(default=0)
    t1pokemon3death=models.IntegerField(default=0)
    t1pokemon4death=models.IntegerField(default=0)
    t1pokemon5death=models.IntegerField(default=0)
    t1pokemon6death=models.IntegerField(default=0)
    t2pokemon1death=models.IntegerField(default=0)
    t2pokemon2death=models.IntegerField(default=0)
    t2pokemon3death=models.IntegerField(default=0)
    t2pokemon4death=models.IntegerField(default=0)
    t2pokemon5death=models.IntegerField(default=0)
    t2pokemon6death=models.IntegerField(default=0)
    winner=models.ForeignKey(coachdata,on_delete=models.CASCADE)
    t1forfeit=models.BooleanField(default="False")
    t2forfeit=models.BooleanField(default="False")

class match_replay(models.Model):
    match=models.OneToOneField(schedule,on_delete=models.CASCADE)
    data=JSONField()