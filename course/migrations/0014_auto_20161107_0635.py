# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_auto_20161106_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolledcourse',
            name='completion_date',
            field=models.DateTimeField(),
        ),
    ]
