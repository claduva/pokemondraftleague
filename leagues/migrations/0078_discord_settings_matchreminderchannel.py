# Generated by Django 2.2.10 on 2020-10-24 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0077_auto_20200424_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='discord_settings',
            name='matchreminderchannel',
            field=models.CharField(default='Not Provided', max_length=100),
        ),
    ]