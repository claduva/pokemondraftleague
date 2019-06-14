# Generated by Django 2.1.7 on 2019-06-14 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_league_team_alternate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coachaward',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coachdata',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaching', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='coachdata',
            name='logo',
            field=models.ImageField(blank=True, default='team_logos/defaultteamlogo.png', null=True, upload_to='team_logos'),
        ),
        migrations.AlterField(
            model_name='league',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosting', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='league',
            name='logo',
            field=models.ImageField(blank=True, default='league_logos/defaultleaguelogo.png', null=True, upload_to='league_logos'),
        ),
        migrations.AlterField(
            model_name='league_settings',
            name='league_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='leagues.league'),
        ),
        migrations.AlterField(
            model_name='league_team',
            name='alternate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alternate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='league_team',
            name='logo',
            field=models.ImageField(blank=True, default='league_logos/defaultleaguelogo.png', null=True, upload_to='team_logos'),
        ),
    ]
