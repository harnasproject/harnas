# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('contest', '0017_auto_20160308_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTaskDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('close', models.DateTimeField()),
                ('group', models.ForeignKey(to='auth.Group')),
                ('task', models.ForeignKey(to='contest.Task')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='grouptaskdetails',
            index_together=set([('group', 'task')]),
        ),
    ]
