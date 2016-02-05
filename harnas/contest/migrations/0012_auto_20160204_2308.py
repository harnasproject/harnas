# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0011_auto_20160105_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': (('view', 'Can view'), ('submit', 'Can submit solution'), ('edit', 'Can edit'), ('delete', 'Can delete'))},
        ),
    ]
