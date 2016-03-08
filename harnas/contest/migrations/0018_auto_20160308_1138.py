# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0017_auto_20160305_1618'),
    ]

    operations = [
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
            field=models.ForeignKey(default=None, null=True, to='contest.Contest'),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(default=None, null=True, to='contest.Task'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(unique=True, max_length=250),
        ),
        migrations.DeleteModel(
            name='TaskEdition',
        ),
    ]
