# Generated by Django 2.1.7 on 2019-05-03 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0002_auto_20190503_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon_tier',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.league'),
        ),
    ]
