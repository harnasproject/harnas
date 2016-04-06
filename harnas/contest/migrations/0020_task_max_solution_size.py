# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0019_auto_20160308_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='max_solution_size',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
