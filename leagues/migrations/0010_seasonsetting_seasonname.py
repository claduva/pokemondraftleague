# Generated by Django 2.1.7 on 2019-05-05 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0009_auto_20190505_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonsetting',
            name='seasonname',
            field=models.CharField(default='Season 1', max_length=25),
        ),
    ]
