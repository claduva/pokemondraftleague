# Generated by Django 2.1.7 on 2019-05-02 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awardname', models.CharField(default='None', max_length=20)),
                ('image', models.ImageField(blank=True, default='profile_pics/defaultpfp.png', null=True, upload_to='awards')),
            ],
        ),
        migrations.CreateModel(
            name='coachaward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.award')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
