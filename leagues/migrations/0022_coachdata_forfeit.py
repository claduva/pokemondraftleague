# Generated by Django 2.1.7 on 2019-05-09 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0021_auto_20190509_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachdata',
            name='forfeit',
            field=models.IntegerField(default=0),
        ),
    ]
