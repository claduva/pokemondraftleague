from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image

from leagues.models import *

class all_pokemon(models.Model):
    pokemon = models.CharField(max_length=30)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    s_attack = models.IntegerField()
    s_defense = models.IntegerField()
    speed = models.IntegerField()
    is_fully_evolved = models.BooleanField()

class pokemon_type(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    typing = models.CharField(max_length=15)

class pokemon_ability(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    ability = models.CharField(max_length=30)

class moveinfo(models.Model):
    name = models.CharField(max_length=50)
    move_typing = models.CharField(max_length=10)
    move_category = models.CharField(max_length=10)
    move_power = models.IntegerField()
    move_accuracy = models.IntegerField()
    move_priority = models.IntegerField()
    secondary_effect_chance = models.IntegerField()
    secondary_effect = models.CharField(max_length=100)

class pokemon_moveset(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)

class pokemon_tier(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    league = models.ForeignKey(league,on_delete=models.CASCADE)
    points = models.IntegerField(default=0) 