# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0009_auto_20160102_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='contest_id',
            new_name='contest',
        ),
    ]
