# Generated by Django 2.1.7 on 2019-06-20 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_discordid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='discordid',
            field=models.BigIntegerField(null=True),
        ),
    ]