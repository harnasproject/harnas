# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20160205_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='contest',
            field=models.ForeignKey(null=True, default=None, to='contest.Contest'),
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(null=True, default=None, to='contest.Task'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='comparator',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='executor',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='in_file_path',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='out_file_path',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='name',
            field=models.CharField(unique=True, max_length=250),
        ),
    ]
