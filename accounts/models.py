from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage as storage
from PIL import Image

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=30, null=True,blank=True)
    pfp = models.ImageField(default='profile_pics/defaultpfp.png',upload_to='profile_pics',null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        if self.pfp:
            size = 300, 300
            image = Image.open(self.pfp)
            image.thumbnail(size, Image.ANTIALIAS)
            fh = storage.open(self.pfp.name, "w")
            #format = 'png'  # You need to set the correct image format here
            image.save(fh)#,format)
            fh.close()