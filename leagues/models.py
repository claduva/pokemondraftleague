from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage

from enum import Enum



class league(models.Model):
    name = models.CharField(max_length=30, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE,related_name='hosting')
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='league_logos',null=True, blank=True)

    def __str__(self):
        return f'{self.name} hosted by {self.host.username}'

class league_settings(models.Model):
    league_name = models.OneToOneField(league, on_delete=models.CASCADE,related_name="settings")
    number_of_teams = models.IntegerField(default=16)
    number_of_conferences = models.IntegerField(default=2)
    number_of_divisions = models.IntegerField(default=2)
    is_recruiting = models.BooleanField(default=True)
    allows_teams = models.BooleanField(default=False)
    teambased = models.BooleanField(default=False)
    discordurl = models.CharField(max_length=100, default="Not Provided")
    discordserver = models.CharField(max_length=100, default="Not Provided")
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f'League settings for {self.league_name.name}'

class conference_name(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

class division_name(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    associatedconference = models.ForeignKey(conference_name, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

class league_application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    league_name = models.ForeignKey(league, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.applicant.username}\'s application for {self.league_name.name}'

class league_team(models.Model):
    league=models.ForeignKey(league,on_delete=models.CASCADE,related_name="leagueteam")
    name=models.CharField(max_length=50,default="Not Specified")
    logo = models.ImageField(default='league_logos/defaultleaguelogo.png',upload_to='team_logos',null=True, blank=True)
    alternate=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='alternate')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)

class coachdata(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE,related_name='coaching')
    league_name = models.ForeignKey(league, on_delete=models.CASCADE)
    logo = models.ImageField(default='team_logos/defaultteamlogo.png',upload_to='team_logos',null=True, blank=True)
    teamabbreviation = models.CharField(max_length=3, default="TBD")
    teamname = models.CharField(max_length=100, default="To Be Determined")
    teammate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='teammate')
    parent_team = models.ForeignKey(league_team, on_delete=models.SET_NULL, null=True)
    conference = models.ForeignKey(conference_name, on_delete=models.SET_NULL, null=True)
    division = models.ForeignKey(division_name, on_delete=models.SET_NULL, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    forfeit = models.IntegerField(default=0)

    def __str__(self):
        if self.teammate != None:
            teammate=f' and {self.teammate.username}'
        else:
            teammate=''
        return f'{self.league_name.name}: {self.coach.username}{teammate}'

class award(models.Model):
    awardname = models.CharField(max_length=20, default="None",unique=True)
    image = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='awards',null=True, blank=True)
    
    def __str__(self):
        return f'Award: {self.awardname}'

class coachaward(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE,related_name='awards')
    award = models.ForeignKey(award, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.award.awardname} for {self.coach.username}'

class leaguetiers(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    tiername = models.CharField(max_length=20, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

    def __str__(self):
        return f'Tier for {self.league.name}, Tiername: {self.tiername}'

class leaguetiertemplate(models.Model):
    template = models.CharField(max_length=25, default="Standard Draft League")
    tiername = models.CharField(max_length=20, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

    def __str__(self):
        return f'Template: {self.template}, Tiername: {self.tiername}'

class seasonsetting(models.Model):
    league = models.OneToOneField(league, on_delete=models.CASCADE)
    seasonname= models.CharField(max_length=25, default="Season 1")
    draftstart=models.DateTimeField(null=True)
    drafttimer=models.IntegerField(default=12)
    draftbudget = models.IntegerField(default=1080)
    picksperteam = models.IntegerField(default=12)
    drafttype = models.CharField(max_length=25, choices=(
        ("Snake","Snake"),
        ),
        default="Snake")
    seasonstart=models.DateTimeField(null=True)
    seasonlength = models.IntegerField(default=7)
    freeagenciesallowed= models.IntegerField(default=4)
    tradesallowed= models.IntegerField(default=4)
    numzusers= models.IntegerField(default=2)
    candeletez = models.BooleanField(default=False)

    def __str__(self):
        return f'League: {self.league.name}, Season: {self.seasonname}'

from pokemondatabase.models import all_pokemon

class roster(models.Model):
    season = models.ForeignKey(seasonsetting, on_delete=models.CASCADE)
    team = models.ForeignKey(coachdata, on_delete=models.CASCADE,null=True)
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True)
    kills = models.IntegerField(default=0)
    deaths =  models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    zuser = models.CharField(max_length=20,choices=(
        ("OS","Offensive and Status"),
        ("O","Offensive"),
        ("N","None"),
        ),
        default="N")

    def __str__(self):
        return f'Roster for League: {self.season.league.name}, Season: {self.season.seasonname}'

class draft(models.Model):
    season = models.ForeignKey(seasonsetting, on_delete=models.CASCADE)
    team = models.ForeignKey(coachdata, on_delete=models.CASCADE,null=True,related_name="draftpicks")
    pokemon = models.ForeignKey(all_pokemon, on_delete=models.CASCADE,null=True)
    picktime= models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Draft {self.id}, League: {self.season.league.name}, Season: {self.season.seasonname}'

class draft_announcements(models.Model):
    league = models.CharField(max_length=100)
    league_name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    announced = models.BooleanField(default=False)
    upnext = models.CharField(max_length=100,null=True)