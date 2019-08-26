# Generated by Django 2.1.7 on 2019-08-21 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leagues', '0031_auto_20190726_1618'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pokemondatabase', '0005_auto_20190715_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='planned_draft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draftname', models.CharField(max_length=100)),
                ('associatedleague', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leagues.league')),
                ('pokemonlist', models.ManyToManyField(to='pokemondatabase.all_pokemon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]