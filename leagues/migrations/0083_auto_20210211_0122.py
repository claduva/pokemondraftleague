# Generated by Django 2.2.10 on 2021-02-11 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0082_auto_20210211_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='logourl',
            field=models.URLField(blank=True, default='https://i.imgur.com/wAFIg59.png', max_length=400),
        ),
    ]