# Generated by Django 2.2.10 on 2020-03-03 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0068_auto_20200217_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coachdata',
            options={'ordering': ['league_name', 'subleague', 'coach']},
        ),
        migrations.AlterModelOptions(
            name='seasonsetting',
            options={'ordering': ['league']},
        ),
    ]
