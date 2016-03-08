# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0018_taskedition_contest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskedition',
            name='contest',
        ),
        migrations.RemoveField(
            model_name='taskedition',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='taskedition',
            name='task_ptr',
        ),
        migrations.AddField(
            model_name='task',
            name='contest',
            field=models.ForeignKey(null=True, default=None, to='contest.Contest'),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(null=True, default=None, to='contest.Task'),
        ),
        migrations.DeleteModel(
            name='TaskEdition',
        ),
    ]
