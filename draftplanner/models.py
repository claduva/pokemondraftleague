from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
import urllib
import os
from enum import Enum

from leagues.models import *
from pokemondatabase.models import *

class planned_draft(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    associatedleague = models.ForeignKey(league_subleague, on_delete=models.CASCADE, null=True)
    draftname = models.CharField(max_length=100)
    pokemonlist = models.ManyToManyField(all_pokemon)
