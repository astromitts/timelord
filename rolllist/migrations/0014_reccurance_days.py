# Generated by Django 2.2.1 on 2019-07-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0013_populate_day_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_0',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_5',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recurringscheduleitem',
            name='recurrance_6',
            field=models.BooleanField(default=False),
        ),
    ]
