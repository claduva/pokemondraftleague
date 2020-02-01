from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image
from enum import Enum

from individualleague.models import *

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=30, null=True,blank=True)
    pfp = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='profile_pics',null=True, blank=True)
    discordid = models.BigIntegerField(null=True,help_text="Right click yourself in the Discord right sidebar and click 'Copy ID'")
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    seasonsplayed = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

class showdownalts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="showdownalts")
    showdownalt = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return f'Showdown Alt ({self.showdownalt})for {self.user.username}'

class sitesettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sprite = models.CharField(max_length=30,choices=(
        ("swsh/ani/standard/PKMN.gif","Current Animated"),
        ("swsh/ani/shiny/PKMN.gif","Current Shiny Animated"),
        ("swsh/png/standard/PKMN.png","Current"),
        ("swsh/png/shiny/PKMN.png","Current Shiny"),
        ("bw/png/standard/PKMN.png","BW"),
        ("bw/png/shiny/PKMN.png","BW Shiny"),
        ("afd/png/standard/PKMN.png","April Fools Day"),
        ("afd/png/shiny/PKMN.png","April Fools Day Shiny"),
        ),
        default="swsh/ani/standard/PKMN.gif")
    
    def __str__(self):
        return f'Site settings for {self.user.username}'

class inbox(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='recipient')
    messagesubject=models.TextField(default="Message Subject")
    messagebody=models.TextField()
    senttime=models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)