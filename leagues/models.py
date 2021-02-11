from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage

from enum import Enum
from multiselectfield import MultiSelectField

class league(models.Model):
    name = models.CharField(max_length=30, unique=True)
    host = models.ManyToManyField(User,related_name='hosting')
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='league_logos',null=True, blank=True)
    logourl = models.URLField(max_length=400,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

class league_settings(models.Model):
    league_name = models.OneToOneField(league, on_delete=models.CASCADE,related_name="settings")
    is_recruiting = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    platform=models.CharField(max_length=30,choices=(
        ('Youtube Showdown','Youtube Showdown'),
        ('Youtube Wifi','Youtube Wifi'),
        ('Showdown','Showdown'),
        ('Wifi','Wifi'),
    ),default="Showdown")
    metagame=MultiSelectField(choices=(
        ('Gen 8 National Dex','Gen 8 National Dex'),
        ('Gen 8 Galar Dex','Gen 8 Galar Dex'),
        ('Gen 8 Ubers','Gen 8 Ubers'),
        ('Gen 8 T3 & Below','Gen 8 T3 & Below'),
        ('Gen 8 LC','Gen 8 LC'),
        ('Pre Gen 8','Pre Gen 8'),
    ),default="Gen 8 National Dex")

    def __str__(self):
        return f'League settings for {self.league_name.name}'

class league_configuration(models.Model):
    league = models.OneToOneField(league, on_delete=models.CASCADE,related_name="configuration")
    number_of_subleagues = models.IntegerField(default=1)
    allows_cross_subleague_matches = models.BooleanField(default=False)
    allows_teams = models.BooleanField(default=False)
    teambased = models.BooleanField(default=False)

    def __str__(self):
        return f'League configuration for {self.league.name}'

class league_subleague(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name="subleague")
    subleague = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.league.name}: {self.subleague}'

class discord_settings(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name="discord_settings")
    subleague = models.OneToOneField(league_subleague,on_delete=models.SET_NULL, null=True)
    discordurl = models.CharField(max_length=100, default="Not Provided")
    discordserver = models.CharField(max_length=100, default="Not Provided")
    draftchannel=models.CharField(max_length=100, default="Not Provided")
    freeagencychannel=models.CharField(max_length=100, default="Not Provided")
    tradechannel=models.CharField(max_length=100, default="Not Provided")
    replaychannel=models.CharField(max_length=100, default="Not Provided")
    matchreminderchannel=models.CharField(max_length=100, default="Not Provided")
    
    def __str__(self):
        return f'Discord settings for {self.league.name}'

class conference_name(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name="conferences")
    subleague = models.ForeignKey(league_subleague,on_delete=models.CASCADE, related_name="subleague_conferences")
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class division_name(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    subleague = models.ForeignKey(league_subleague,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    associatedconference = models.ForeignKey(conference_name, on_delete=models.CASCADE,related_name='divisions')

    def __str__(self):
        return f'{self.name}'

class league_application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    league_name = models.ForeignKey(league, on_delete=models.CASCADE)
    discord_name = models.CharField(max_length=50,default="None")
    teamabbreviation = models.CharField(max_length=3, default="TBD")
    teamname = models.CharField(max_length=100, default="To Be Determined")
    draft_league_resume = models.TextField(default="None")
    tier_preference = models.ManyToManyField(league_subleague,related_name='apptiers')
    willingtobealternate = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.applicant.username}\'s application for {self.league_name.name}'

class league_team(models.Model):
    league=models.ForeignKey(league,on_delete=models.CASCADE,related_name="leagueteam")
    name=models.CharField(max_length=50,default="Not Specified")
    shortname=models.CharField(max_length=50,default="Not Specified")
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='team_logos',null=True, blank=True)
    logourl = models.URLField(default="https://i.imgur.com/buHiZ1x.png",max_length=400,blank=True)
    captain=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='alternate')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)

class teamlogo(models.Model):
    logo = models.ImageField(default='team_logos/defaultteamlogo.png',upload_to='team_logos',null=True, blank=True)
    logourl = models.URLField(default="https://i.imgur.com/buHiZ1x.png",max_length=400,blank=True)

class coachdata(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE,related_name='coaching')
    league_name = models.ForeignKey(league, on_delete=models.CASCADE,related_name="leagueteams")
    logo = models.ImageField(default='team_logos/defaultteamlogo.png',upload_to='team_logos',null=True, blank=True)
    logo2=models.ForeignKey(teamlogo, on_delete=models.SET_NULL, null=True)
    logourl = models.URLField(default="https://i.imgur.com/buHiZ1x.png",max_length=400,blank=True)
    teamabbreviation = models.CharField(max_length=3, default="TBD")
    teamname = models.CharField(max_length=100, default="To Be Determined")
    teammate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='teammate')
    parent_team = models.ForeignKey(league_team, on_delete=models.SET_NULL, null=True,related_name="child_teams")
    subleague = models.ForeignKey(league_subleague,on_delete=models.CASCADE, null=True,related_name='subleague_coachs')
    conference = models.ForeignKey(conference_name, on_delete=models.SET_NULL, null=True,related_name='conferenceteams')
    division = models.ForeignKey(division_name, on_delete=models.SET_NULL, null=True,related_name='divisionteams')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    forfeit = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

    def __str__(self):
        if self.teammate != None:
            teammate=f' and {self.teammate.username}'
        else:
            teammate=''
        return f'{self.league_name.name}: {self.coach.username}{teammate}'
    
    class Meta:
        ordering = ['league_name','subleague','coach']

class award(models.Model):
    awardname = models.CharField(max_length=50, default="None",unique=True)
    image = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='awards',null=True, blank=True)
    ordering=models.IntegerField(default=0)
    def __str__(self):
        return f'Award: {self.awardname}'

class coachaward(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE,related_name='awards')
    award = models.ForeignKey(award, on_delete=models.CASCADE)
    text = models.CharField(max_length=200,default=None)
    timeawarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['award__ordering','-text']
        unique_together = (("coach", "award",'text'),)  

    def __str__(self):
        return f'{self.award.awardname} for {self.coach.username}'

class leaguetiers(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name='leaguetiers')
    subleague = models.ForeignKey(league_subleague,on_delete=models.CASCADE, null=True,related_name='subleaguetiers')
    tiername = models.CharField(max_length=20, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

    class Meta:
        ordering = ['league']

    def __str__(self):
        return f'Tier for {self.league.name}-{self.subleague}, Tiername: {self.tiername}'

class leaguetiertemplate(models.Model):
    template = models.CharField(max_length=50, default="Standard Draft League")
    tiername = models.CharField(max_length=50, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

    def __str__(self):
        return f'Template: {self.template}, Tiername: {self.tiername}'

class seasonsetting(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    subleague = models.OneToOneField(league_subleague,on_delete=models.CASCADE, null=True)
    seasonname= models.CharField(max_length=25, default="Season 1")
    number_of_teams = models.IntegerField(default=16)
    number_of_conferences = models.IntegerField(default=2)
    number_of_divisions = models.IntegerField(default=2)
    draftstart=models.DateTimeField(null=True)
    drafttimer=models.IntegerField(default=12)
    draftbudget = models.IntegerField(default=1080)
    picksperteam = models.IntegerField(default=11)
    drafttype = models.CharField(max_length=25, choices=(
        ("Snake","Snake"),
        ),
        default="Snake")
    seasonstart=models.DateTimeField(null=True)
    seasonlength = models.IntegerField(default=7)
    playoffslength = models.IntegerField(default=3)
    freeagenciesallowed= models.IntegerField(default=4)
    tradesallowed= models.IntegerField(default=4)
    numzusers= models.IntegerField(default=2)
    candeletez = models.BooleanField(default=False)
    playoffteamsperconference= models.IntegerField(default=4)

    def __str__(self):
        return f'League: {self.league.name}, Subeague: {self.subleague.subleague}, Season: {self.seasonname}'

    class Meta:
        ordering = ['league']

from pokemondatabase.models import all_pokemon

class roster(models.Model):
    season = models.ForeignKey(seasonsetting, on_delete=models.CASCADE)
    team = models.ForeignKey(coachdata, on_delete=models.CASCADE,null=True,related_name='teamroster')
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="pokemonroster")
    kills = models.IntegerField(default=0)
    deaths =  models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)
    zuser = models.CharField(max_length=20,choices=(
        ("OS","Offensive and Status"),
        ("O","Offensive"),
        ("N","None"),
        ),
        default="N")

    def __str__(self):
        if self.pokemon==None:
            return f'Roster for League: {self.season.league.name}, Season: {self.season.seasonname}. No draftpick yet'
        else:
            return f'Roster for League: {self.season.league.name}, Season: {self.season.seasonname}, Pokemon: {self.pokemon.pokemon}'

class draft(models.Model):
    season = models.ForeignKey(seasonsetting, on_delete=models.CASCADE)
    picknumber = models.IntegerField(default=0)
    team = models.ForeignKey(coachdata, on_delete=models.CASCADE,null=True,related_name="draftpicks")
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True,related_name="pokemondraft")
    picktime= models.DateTimeField(auto_now=True, null=True)
    skipped= models.BooleanField(default=False)
    announced= models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    @property
    def upnext(self):
        try:
            un=draft.objects.filter(season=self.season).get(picknumber=self.picknumber+1)
            un=f'{un.team.teamname}, coached by {un.team.coach.username},' 
        except:
            un="The draft has concluded."
        return un
    
    @property
    def upnextid(self):
        try:
            unid=draft.objects.filter(season=self.season).get(picknumber=self.picknumber+1)
            unid=unid.team.coach.profile.discordid
        except:
            unid=None
        return unid

    def __str__(self):
        return f'Draft {self.id}, League: {self.season.league.name}, Season: {self.season.seasonname}'