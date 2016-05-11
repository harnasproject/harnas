# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0020_task_max_solution_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='name',
            field=models.CharField(max_length=100, default=None, null=True),
        ),
        migrations.AddField(
            model_name='testcase',
            name='run_order_id',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
