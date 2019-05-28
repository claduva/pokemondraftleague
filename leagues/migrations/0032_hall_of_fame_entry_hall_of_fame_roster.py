# Generated by Django 2.1.7 on 2019-05-23 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0009_auto_20190517_2045'),
        ('leagues', '0031_seasonsetting_drafttimer'),
    ]

    operations = [
        migrations.CreateModel(
            name='hall_of_fame_entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seasonname', models.CharField(default='Not Specified', max_length=20)),
                ('championteamname', models.CharField(default='Not Specified', max_length=50)),
                ('runnerupteamname', models.CharField(default='Not Specified', max_length=50)),
                ('championshipreplay', models.CharField(default='Not Specified', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='hall_of_fame_roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hall_of_frame_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.hall_of_fame_entry')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemondatabase.all_pokemon')),
            ],
        ),
    ]