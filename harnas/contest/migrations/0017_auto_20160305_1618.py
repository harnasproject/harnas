# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20160205_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskEdition',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='contest.Task', primary_key=True, serialize=False)),
                ('parent', models.ForeignKey(to='contest.Task', related_name='child_tasks')),
            ],
            bases=('contest.task',),
        ),
        migrations.AddField(
            model_name='testcase',
            name='comparator',
            field=models.CharField(max_length=500, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='executor',
            field=models.CharField(max_length=500, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='in_file_path',
            field=models.CharField(max_length=500, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='out_file_path',
            field=models.CharField(max_length=500, default=''),
            preserve_default=False,
        ),
    ]
