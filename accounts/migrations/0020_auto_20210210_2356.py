# Generated by Django 2.2.10 on 2021-02-10 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_profile_pfpurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pfpurl',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]
