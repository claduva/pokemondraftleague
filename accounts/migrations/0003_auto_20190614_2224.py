# Generated by Django 2.1.7 on 2019-06-14 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_inbox_traderequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='differential',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='gp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='gw',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
