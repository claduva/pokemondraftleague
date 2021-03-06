# Generated by Django 2.1.7 on 2019-09-11 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0040_auto_20190911_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference_name',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
        migrations.AddField(
            model_name='discord_settings',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
        migrations.AddField(
            model_name='division_name',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
        migrations.AddField(
            model_name='leaguetiers',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
        migrations.AddField(
            model_name='seasonsetting',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
    ]
