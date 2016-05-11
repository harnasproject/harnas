# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0021_auto_20160504_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='in_file_path',
            field=models.FilePathField(max_length=500),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='out_file_path',
            field=models.FilePathField(max_length=500),
        ),
    ]
