# Generated by Django 2.1.7 on 2019-07-15 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('individualleague', '0015_auto_20190709_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='team1alternateattribution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team1alternateattribution', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schedule',
            name='team2alternateattribution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team2alternateattribution', to=settings.AUTH_USER_MODEL),
        ),
    ]
