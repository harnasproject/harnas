# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0005_auto_20151220_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 23, 18, 5, 42, 725410, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 23, 18, 5, 48, 710666, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
