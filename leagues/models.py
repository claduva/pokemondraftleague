from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image

class league(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='league_logos',null=True, blank=True)

    """ def save(self):
        super().save()
        if self.logo:
            size = 300, 300
            image = Image.open(self.logo)
            image.thumbnail(size, Image.ANTIALIAS)
            fh = storage.open(self.logo.name, "w")
            #format = 'png'  # You need to set the correct image format here
            image.save(fh)#,format)
            fh.close() """

class league_settings(models.Model):
    league_name = models.OneToOneField(league, on_delete=models.CASCADE)
    number_of_teams = models.IntegerField(default=16)
    number_of_conferences = models.IntegerField(default=2)
    number_of_divisions = models.IntegerField(default=2)
    is_recruiting = models.BooleanField(default=True)
    allows_teams = models.BooleanField(default=False)
    discordurl = models.CharField(max_length=100, default="Not Provided")

class league_application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    league_name = models.ForeignKey(league, on_delete=models.CASCADE)

class coachdata(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE)
    league_name = models.ForeignKey(league, on_delete=models.CASCADE)
    logo = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='team_logos',null=True, blank=True)
    teamabbreviation = models.CharField(max_length=3, default="TBD")
    teamname = models.CharField(max_length=100, default="To Be Determined")
    teammate = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='teammate')

class award(models.Model):
    awardname = models.CharField(max_length=20, default="None")
    image = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='awards',null=True, blank=True)
    
class coachaward(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE)
    award = models.ForeignKey(award, on_delete=models.CASCADE)

class leaguetiers(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    tiername = models.CharField(max_length=20, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

class leaguetiertemplate(models.Model):
    template = models.CharField(max_length=25, default="Standard Draft League")
    tiername = models.CharField(max_length=20, default="Not Specified")
    tierpoints = models.IntegerField(default=0)

