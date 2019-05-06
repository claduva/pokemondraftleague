# Generated by Django 2.1.7 on 2019-05-06 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leagues', '0015_draft_pickstart'),
    ]

    operations = [
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('team1score', models.IntegerField(default=0)),
                ('team2score', models.IntegerField(default=0)),
                ('replay', models.CharField(max_length=100)),
                ('team1usedz', models.BooleanField(default=False)),
                ('team2usedz', models.BooleanField(default=False)),
                ('team1megaevolved', models.BooleanField(default=False)),
                ('team2megaevolved', models.BooleanField(default=False)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.seasonsetting')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='leagues.coachdata')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='leagues.coachdata')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='leagues.coachdata')),
            ],
        ),
    ]
