# Generated by Django 2.1.7 on 2019-05-01 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0003_league_settings_is_recruiting'),
    ]

    operations = [
        migrations.AddField(
            model_name='league_settings',
            name='discordurl',
            field=models.CharField(default='Not Provided', max_length=100),
        ),
    ]
