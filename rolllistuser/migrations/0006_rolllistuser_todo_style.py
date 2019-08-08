# Generated by Django 2.2.1 on 2019-08-08 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rolllistuser', '0005_add_schedule_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolllistuser',
            name='todo_style',
            field=models.CharField(choices=[('checkbox', 'Checkbox style'), ('kanban', 'Kanban style')], default='checkbox', max_length=120),
            preserve_default=False,
        ),
    ]
