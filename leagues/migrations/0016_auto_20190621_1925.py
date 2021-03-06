# Generated by Django 2.1.7 on 2019-06-21 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0015_auto_20190620_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='discord_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draftchannel', models.CharField(default='Not Provided', max_length=100)),
                ('freeagencychannel', models.CharField(default='Not Provided', max_length=100)),
                ('tradechannel', models.CharField(default='Not Provided', max_length=100)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='discord_settings', to='leagues.league')),
            ],
        ),
        migrations.AlterField(
            model_name='division_name',
            name='associatedconference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='leagues.conference_name'),
        ),
    ]
