# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 15:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='instructor_id',
            new_name='instructor',
        ),
        migrations.RenameField(
            model_name='enrolledcourse',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='enrolledcourse',
            old_name='status_id',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='enrolledcourse',
            old_name='user_id',
            new_name='user',
        ),
    ]
