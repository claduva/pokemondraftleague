# Generated by Django 2.1.7 on 2019-07-03 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('individualleague', '0011_trade_request_league'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade_request',
            name='league',
        ),
    ]