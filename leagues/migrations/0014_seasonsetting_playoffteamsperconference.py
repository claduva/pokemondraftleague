# Generated by Django 2.1.7 on 2019-06-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0013_draft_announcements_upnext'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonsetting',
            name='playoffteamsperconference',
            field=models.IntegerField(default=4),
        ),
    ]