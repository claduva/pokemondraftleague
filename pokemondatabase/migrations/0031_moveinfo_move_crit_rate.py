# Generated by Django 2.2.10 on 2020-06-18 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0030_unmatched_moves'),
    ]

    operations = [
        migrations.AddField(
            model_name='moveinfo',
            name='move_crit_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
