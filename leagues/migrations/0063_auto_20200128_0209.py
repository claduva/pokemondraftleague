# Generated by Django 2.1.7 on 2020-01-28 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0062_auto_20200126_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference_name',
            name='subleague',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subleague_conferences', to='leagues.league_subleague'),
        ),
    ]
