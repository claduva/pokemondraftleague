# Generated by Django 2.1.7 on 2019-09-09 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0034_league_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='league_subleague',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subleague', models.CharField(max_length=30)),
                ('league', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subleague', to='leagues.league')),
            ],
        ),
    ]
