# Generated by Django 2.1.7 on 2019-07-09 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('individualleague', '0014_pickems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickems',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pickems', to=settings.AUTH_USER_MODEL),
        ),
    ]
