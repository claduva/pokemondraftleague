# Generated by Django 2.1.7 on 2019-09-09 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0037_auto_20190909_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachdata',
            name='subleague',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.league_subleague'),
        ),
    ]
