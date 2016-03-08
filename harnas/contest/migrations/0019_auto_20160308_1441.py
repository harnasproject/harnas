# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0018_auto_20160308_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='close',
            field=models.DateTimeField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='task',
            name='open',
            field=models.DateTimeField(null=True, default=None),
        ),
    ]
