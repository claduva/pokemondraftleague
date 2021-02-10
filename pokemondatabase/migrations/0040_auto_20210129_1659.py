# Generated by Django 2.2.10 on 2021-01-29 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemondatabase', '0039_auto_20201024_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon_sprites',
            name='afdshinyurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='afdurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='bwshinyurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='bwurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='dexanishinyurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='dexaniurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='dexshinyurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
        migrations.AddField(
            model_name='pokemon_sprites',
            name='dexurl',
            field=models.URLField(default='https://claduva.github.io/pdl_images/sprites/default.png', max_length=500),
        ),
    ]