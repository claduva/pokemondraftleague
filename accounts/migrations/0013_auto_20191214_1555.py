# Generated by Django 2.1.7 on 2019-12-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20191214_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='sprite',
            field=models.CharField(choices=[('swsh/ani/standard/PKMN.gif', 'Current Animated'), ('swsh/ani/shiny/PKMN.gif', 'Current Shiny Animated'), ('swsh/png/standard/PKMN.png', 'Current'), ('swsh/png/shiny/PKMN.png', 'Current Shiny'), ('bw/png/standard/PKMN.png', 'BW'), ('bw/png/shiny/PKMN.png', 'BW Shiny'), ('afd/png/standard/PKMN.png', 'April Fools Day'), ('afd/png/shiny/PKMN.png', 'April Fools Day Shiny')], default='swsh/ani/standard/PKMN.gif', max_length=30),
        ),
    ]
