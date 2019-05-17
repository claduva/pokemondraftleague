from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image

from leagues.models import league,leaguetiers,leaguetiertemplate

class all_pokemon(models.Model):
    pokemon = models.CharField(max_length=30,unique=True)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    s_attack = models.IntegerField()
    s_defense = models.IntegerField()
    speed = models.IntegerField()
    is_fully_evolved = models.BooleanField()
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    timesdrafted = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pokemon}'

class pokemon_type(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    typing = models.CharField(max_length=15)

    def __str__(self):
        return f'Typing for {self.pokemon.pokemon}'

class pokemon_ability(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    ability = models.CharField(max_length=30)

    def __str__(self):
        return f'Ability for {self.pokemon.pokemon}'

class moveinfo(models.Model):
    name = models.CharField(max_length=50,unique=True)
    move_typing = models.CharField(max_length=10)
    move_category = models.CharField(max_length=10)
    move_power = models.IntegerField()
    move_accuracy = models.IntegerField()
    move_priority = models.IntegerField()
    secondary_effect_chance = models.IntegerField()
    secondary_effect = models.CharField(max_length=100)

    def __str__(self):
        return f'Moveinfo for {self.name}'

class pokemon_moveset(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)

    def __str__(self):
        return f'Moveset data for {self.pokemon.pokemon}'

class pokemon_tier(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    league = models.ForeignKey(league,on_delete=models.CASCADE)
    tier = models.ForeignKey(leaguetiers,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.league.name}: Tiering for {self.pokemon.pokemon}'

class pokemon_tier_template(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    template = models.CharField(max_length=25, default="Standard Draft League")
    tier = models.ForeignKey(leaguetiertemplate,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return f'Template: {self.template}, Pokemon: {self.pokemon.pokemon}'