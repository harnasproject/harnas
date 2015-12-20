# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_news_contest_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('short_name', models.CharField(max_length=3)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('task', models.ForeignKey(to='contest.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TestEnvironment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='test_environment',
            field=models.ForeignKey(to='contest.TestEnvironment'),
        ),
    ]
