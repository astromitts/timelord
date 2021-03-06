# Generated by Django 2.2.1 on 2019-07-09 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0014_reccurance_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='created',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_0',
            field=models.BooleanField(default=False, verbose_name='Monday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_1',
            field=models.BooleanField(default=False, verbose_name='Tuesday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_2',
            field=models.BooleanField(default=False, verbose_name='Wednesday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_3',
            field=models.BooleanField(default=False, verbose_name='Thursday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_4',
            field=models.BooleanField(default=False, verbose_name='Friday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_5',
            field=models.BooleanField(default=False, verbose_name='Saturday'),
        ),
        migrations.AlterField(
            model_name='recurringscheduleitem',
            name='recurrance_6',
            field=models.BooleanField(default=False, verbose_name='Sunday'),
        ),
    ]
