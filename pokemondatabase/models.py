from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from django.contrib.postgres.fields import ArrayField
from PIL import Image
from django.contrib.postgres.fields import JSONField

from leagues.models import league,league_subleague,leaguetiers,leaguetiertemplate

class all_pokemon(models.Model):
    pokemon = models.CharField(max_length=30,unique=True)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    s_attack = models.IntegerField()
    s_defense = models.IntegerField()
    speed = models.IntegerField()
    bst = models.IntegerField(null=True)
    is_fully_evolved = models.BooleanField()
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)
    timesdrafted = models.IntegerField(default=0)
    nicknames = ArrayField(models.CharField(max_length=10, blank=True))
    gen8 = models.BooleanField(default=False)
    canzmove = models.BooleanField(default=True)
    candynamax = models.BooleanField(default=True)
    data=JSONField(null=True)

    def __str__(self):
        return f'{self.pokemon}'

    class Meta:
        ordering = ['pokemon']

class preevolution(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    preevo = models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name="prevos")

    class Meta:
        unique_together = (("pokemon", "preevo"),)

class pokemon_sprites(models.Model):
    pokemon = models.OneToOneField(all_pokemon,on_delete=models.CASCADE,related_name="sprite")
    afd = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/afd/png/standard')
    bw = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/bw/png/standard')
    dex = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/dex/png/standard')
    afdshiny = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/afd/png/shiny')
    bwshiny = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/bw/png/shiny')
    dexshiny = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/dex/png/shiny')
    dexani = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/dex/ani/standard')
    dexanishiny = models.ImageField(default='sprites/sprite_placeholder.gif',upload_to='sprites/dex/ani/shiny')

class pokemon_leaderboard(models.Model):
    pokemon = models.OneToOneField(all_pokemon,on_delete=models.CASCADE)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)
    timesdrafted = models.IntegerField(default=0)

class pokemon_type(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name='types')
    typing = models.CharField(max_length=15)

    class Meta:
        unique_together = (("pokemon", "typing"),)  

    def __str__(self):
        return f'Typing for {self.pokemon.pokemon}'

class pokemon_ability(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name='abilities' )
    ability = models.CharField(max_length=30)

    class Meta:
        unique_together = (("pokemon", "ability"),)  

    def __str__(self):
        return f'Ability for {self.pokemon.pokemon}'

class moveinfo(models.Model):
    name = models.CharField(max_length=50,unique=True)
    altname = models.CharField(max_length=50,default="")
    move_typing = models.CharField(max_length=10)
    move_category = models.CharField(max_length=10)
    move_power = models.IntegerField()
    move_accuracy = models.IntegerField()
    move_priority = models.IntegerField()
    move_crit_rate = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    secondary_effect_chance = models.IntegerField()
    secondary_effect = models.CharField(max_length=100)
    uses = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    crits = models.IntegerField(default=0)
    posssecondaryeffects = models.IntegerField(default=0)
    secondaryeffects = models.IntegerField(default=0)
    
    def __str__(self):
        return f'Moveinfo for {self.name}'

class pokemon_movedata(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)
    uses = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    crits = models.IntegerField(default=0)
    posssecondaryeffects = models.IntegerField(default=0)
    secondaryeffects = models.IntegerField(default=0)

    class Meta:
        unique_together = (("pokemon", "moveinfo"),)  

class user_movedata(models.Model):
    coach = models.ForeignKey(User,on_delete=models.CASCADE)
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)
    uses = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    crits = models.IntegerField(default=0)
    posssecondaryeffects = models.IntegerField(default=0)
    secondaryeffects = models.IntegerField(default=0)

    class Meta:
        unique_together = (("coach", "moveinfo"),)  

class pokemon_moveset(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name='moves')
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)

    class Meta:
        ordering = ['moveinfo__name']
        unique_together = (("pokemon", "moveinfo"),)  

    def __str__(self):
        return f'Moveset data for {self.pokemon.pokemon}'

class unmatched_moves(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    moveinfo = models.ForeignKey(moveinfo,on_delete=models.CASCADE)
    replay = models.CharField(max_length=300,unique=True)

class pokemon_tier(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE,related_name='pokemon_tiers')
    league = models.ForeignKey(league,on_delete=models.CASCADE,related_name='leaguepokemontiers')
    subleague = models.ForeignKey(league_subleague,on_delete=models.CASCADE,related_name='subleaguepokemontiers',null=True)
    tier = models.ForeignKey(leaguetiers,on_delete=models.CASCADE,null=True)
    rosterspot = models.ForeignKey('leagues.roster',on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ['pokemon__pokemon']
        unique_together = (("pokemon", "subleague"),)  

    def __str__(self):
        return f'{self.league.name}: Tiering for {self.pokemon.pokemon}'

class pokemon_tier_template(models.Model):
    pokemon = models.ForeignKey(all_pokemon,on_delete=models.CASCADE)
    template = models.CharField(max_length=50, default="Standard Draft League")
    tier = models.ForeignKey(leaguetiertemplate,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f'Template: {self.template}, Pokemon: {self.pokemon.pokemon}'

    class Meta:
        ordering = ['pokemon__pokemon']

class pokemon_effectiveness(models.Model):
    pokemon = models.OneToOneField(all_pokemon,on_delete=models.CASCADE,related_name="effectiveness")
    bug=models.IntegerField(default=0)
    dark=models.IntegerField(default=0)
    dragon=models.IntegerField(default=0)
    electric=models.IntegerField(default=0)
    fairy=models.IntegerField(default=0)
    fighting=models.IntegerField(default=0)
    fire=models.IntegerField(default=0)
    flying=models.IntegerField(default=0)
    ghost=models.IntegerField(default=0)
    grass=models.IntegerField(default=0)
    ground=models.IntegerField(default=0)
    ice=models.IntegerField(default=0)
    normal=models.IntegerField(default=0)
    poison=models.IntegerField(default=0)
    psychic=models.IntegerField(default=0)
    rock=models.IntegerField(default=0)
    steel=models.IntegerField(default=0)
    water=models.IntegerField(default=0)


    
