# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contest', '0019_auto_20160308_1441'),
        ('checker', '0006_auto_20160305_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('solution', models.BinaryField()),
                ('status', models.CharField(choices=[('QUE', 'In checking queue'), ('MEM', 'Memory limit exceeded'), ('TLE', 'Time limit exceeded'), ('OK', 'Accepted'), ('INT', 'Internal error'), ('ANS', 'Wrong answer'), ('CMP', 'Compilation error'), ('RTE', 'Runtime error')], max_length=3)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='contest.Task')),
            ],
        ),
    ]
