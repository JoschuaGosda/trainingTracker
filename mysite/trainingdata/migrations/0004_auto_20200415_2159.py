# Generated by Django 2.2.11 on 2020-04-15 19:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('trainingdata', '0003_auto_20200415_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customsession',
            name='crimp_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 19, 59, 59, 682613, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='repetitions',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='target',
            field=models.CharField(choices=[('1', 'Fingers'), ('2', 'Upper Body'), ('3', 'Core'), ('4', 'Flexibility'), ('5', 'Antagonists'), ('6', 'Other')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='customsession',
            name='weight',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='deadhang_endurance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 19, 59, 59, 683498, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='deadhang_max',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 19, 59, 59, 683056, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pullup_endurance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 19, 59, 59, 684239, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pullup_max',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 19, 59, 59, 683899, tzinfo=utc)),
        ),
    ]
