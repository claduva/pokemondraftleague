# Generated by Django 2.2.10 on 2020-03-17 20:52

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0072_auto_20200313_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='league_settings',
            name='metagame',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Gen 8 National Dex', 'Gen 8 National Dex'), ('Gen 8 Galar Dex', 'Gen 8 Galar Dex'), ('Gen 8 Ubers', 'Gen 8 Ubers'), ('Gen 8 T3 & Below', 'Gen 8 T3 & Below'), ('Gen 8 LC', 'Gen 8 LC'), ('Pre Gen 8', 'Pre Gen 8')], default='Gen 8 National Dex', max_length=82),
        ),
        migrations.AddField(
            model_name='league_settings',
            name='platform',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Youtube Showdown', 'Youtube Showdown'), ('Youtube Wifi', 'Youtube Wifi'), ('Showdown', 'Showdown'), ('Wifi', 'Wifi')], default='Showdown', max_length=43),
        ),
    ]
