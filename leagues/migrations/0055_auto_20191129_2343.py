# Generated by Django 2.1.7 on 2019-11-29 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0054_auto_20191023_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaguetiertemplate',
            name='template',
            field=models.CharField(default='Standard Draft League', max_length=50),
        ),
        migrations.AlterField(
            model_name='leaguetiertemplate',
            name='tiername',
            field=models.CharField(default='Not Specified', max_length=50),
        ),
    ]