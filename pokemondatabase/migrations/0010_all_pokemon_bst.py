# Generated by Django 2.1.7 on 2019-09-10 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0009_auto_20190909_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_pokemon',
            name='bst',
            field=models.IntegerField(null=True),
        ),
    ]
