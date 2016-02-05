# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0012_auto_20160204_2308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': (('view_task', 'Can view'), ('submit_solution', 'Can submit solution'), ('edit_task', 'Can edit'), ('delete_task', 'Can delete'))},
        ),
    ]
