# Generated by Django 2.1.7 on 2019-05-03 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0002_award_coachaward'),
    ]

    operations = [
        migrations.CreateModel(
            name='leaguetiers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiername', models.CharField(default='Not Specified', max_length=20)),
                ('tierpoints', models.IntegerField(default=0)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.league')),
            ],
        ),
    ]