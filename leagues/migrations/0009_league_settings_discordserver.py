# Generated by Django 2.1.7 on 2019-06-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0008_auto_20190619_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='league_settings',
            name='discordserver',
            field=models.CharField(default='Not Provided', max_length=100),
        ),
    ]
