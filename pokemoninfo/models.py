from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image

class pokemon(models.Model):
    pokemon = models.CharField(max_length=30, null=True,blank=True)
    
