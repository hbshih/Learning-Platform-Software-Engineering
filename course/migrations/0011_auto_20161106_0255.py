# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 02:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_auto_20161105_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moduleprogress',
            old_name='enrolled_course_id',
            new_name='enrolled_course',
        ),
    ]
