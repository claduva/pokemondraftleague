# Generated by Django 2.2.10 on 2020-06-10 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0026_auto_20200610_2133'),
    ]

    operations = [
        migrations.CreateModel(
            name='pokemon_movedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uses', models.IntegerField(default=0)),
                ('hits', models.IntegerField(default=0)),
                ('crits', models.IntegerField(default=0)),
                ('posssecondaryeffects', models.IntegerField(default=0)),
                ('secondaryeffects', models.IntegerField(default=0)),
                ('moveinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemondatabase.moveinfo')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pokemondatabase.all_pokemon')),
            ],
        ),
    ]