# Generated by Django 2.1.7 on 2020-02-17 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0067_auto_20200128_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachdata',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subleague_coachs', to='leagues.league_subleague'),
        ),
        migrations.AlterField(
            model_name='seasonsetting',
            name='picksperteam',
            field=models.IntegerField(default=11),
        ),
    ]
