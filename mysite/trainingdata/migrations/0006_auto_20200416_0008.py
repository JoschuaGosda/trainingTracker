# Generated by Django 2.2.11 on 2020-04-15 22:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainingdata', '0005_auto_20200415_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customsession',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 22, 8, 41, 503345, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='repetitions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='sets',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deadhang_endurance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 22, 8, 41, 504212, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='deadhang_max',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 22, 8, 41, 503829, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pullup_endurance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 22, 8, 41, 504951, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pullup_max',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 22, 8, 41, 504617, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]