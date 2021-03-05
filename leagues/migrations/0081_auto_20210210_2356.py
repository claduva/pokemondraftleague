# Generated by Django 2.2.10 on 2021-02-10 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0080_delete_draft_announcements'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachdata',
            name='logourl',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='league',
            name='logourl',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]