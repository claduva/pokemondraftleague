# Generated by Django 2.2.10 on 2020-03-23 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_inbox_traderequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='coachdata',
            field=models.TextField(default='TBD'),
        ),
    ]