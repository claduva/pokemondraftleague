# Generated by Django 2.1.7 on 2019-05-03 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0003_auto_20190503_0240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon_tier',
            name='coach',
        ),
    ]
