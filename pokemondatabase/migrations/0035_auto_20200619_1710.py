# Generated by Django 2.2.10 on 2020-06-19 17:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokemondatabase', '0034_auto_20200618_1950'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pokemon_movedata',
            unique_together={('pokemon', 'moveinfo')},
        ),
        migrations.AlterUniqueTogether(
            name='user_movedata',
            unique_together={('coach', 'moveinfo')},
        ),
    ]
