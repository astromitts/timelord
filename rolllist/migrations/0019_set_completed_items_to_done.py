# Generated by Django 2.2.1 on 2019-08-08 21:19

from django.db import migrations


def forwards(apps, schema_editor):
    ToDoItem = apps.get_model('rolllist', 'ToDoItem')  # noqa
    ToDoItem.objects.filter(completed=True).update(kanban_status='done')


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('rolllist', '0018_todoitem_kanban_status'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
