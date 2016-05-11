# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0008_submit_webhook_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.CharField(max_length=3, choices=[('QUE', 'In checking queue'), ('MEM', 'Memory limit exceeded'), ('TLE', 'Time limit exceeded'), ('OK', 'Accepted'), ('INT', 'Internal error'), ('ANS', 'Wrong answer'), ('CME', 'Compilation error'), ('RTE', 'Runtime error')]),
        ),
    ]
