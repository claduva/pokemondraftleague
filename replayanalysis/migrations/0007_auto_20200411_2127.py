# Generated by Django 2.2.10 on 2020-04-11 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('replayanalysis', '0006_manual_replay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manual_replay',
            name='t1forfeit',
        ),
        migrations.RemoveField(
            model_name='manual_replay',
            name='t1megaevolved',
        ),
        migrations.RemoveField(
            model_name='manual_replay',
            name='t1usedz',
        ),
        migrations.RemoveField(
            model_name='manual_replay',
            name='t2forfeit',
        ),
        migrations.RemoveField(
            model_name='manual_replay',
            name='t2megaevolved',
        ),
        migrations.RemoveField(
            model_name='manual_replay',
            name='t2usedz',
        ),
    ]