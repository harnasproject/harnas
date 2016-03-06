# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20160205_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='comparator',
            field=models.CharField(max_length=500, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='executor',
            field=models.CharField(max_length=500, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='in_file_path',
            field=models.CharField(max_length=500, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='out_file_path',
            field=models.CharField(max_length=500, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
