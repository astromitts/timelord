# Generated by Django 2.2.1 on 2019-07-08 13:15

from django.db import migrations


def forwards(apps, schema_editor):
    Day = apps.get_model('rolllist', 'Day')  # noqa
    days = Day.objects.all()
    for day in days:
        day.save()


def backwards(apps, schema_editor):
    Day = apps.get_model('rolllist', 'Day')  # noqa
    days = Day.objects.all()
    for day in days:
        day.save()


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0012_day__day_of_week'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
