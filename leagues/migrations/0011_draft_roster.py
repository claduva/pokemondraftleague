# Generated by Django 2.1.7 on 2019-05-05 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0008_auto_20190504_1555'),
        ('leagues', '0010_seasonsetting_seasonname'),
    ]

    operations = [
        migrations.CreateModel(
            name='draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemondatabase.all_pokemon')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.seasonsetting')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leagues.coachdata')),
            ],
        ),
        migrations.CreateModel(
            name='roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kills', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('differential', models.IntegerField(default=0)),
                ('gp', models.IntegerField(default=0)),
                ('gw', models.IntegerField(default=0)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemondatabase.all_pokemon')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.seasonsetting')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leagues.coachdata')),
            ],
        ),
    ]
