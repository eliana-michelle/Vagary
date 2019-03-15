# Generated by Django 2.1.5 on 2019-03-15 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20190315_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attraction',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='event',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel',
        ),
        migrations.AddField(
            model_name='trip',
            name='trip_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
