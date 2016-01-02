# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0008_auto_20151229_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='test_environment',
            field=models.ForeignKey(to='checker.TestEnvironment'),
        ),
        migrations.DeleteModel(
            name='TestEnvironment',
        ),
    ]
