# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_auto_20161107_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', embed_video.fields.EmbedVideoField()),
            ],
        ),
    ]
