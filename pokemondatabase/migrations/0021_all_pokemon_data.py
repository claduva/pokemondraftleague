# Generated by Django 2.2.10 on 2020-03-24 19:02

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0020_moveinfo_altname'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_pokemon',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
