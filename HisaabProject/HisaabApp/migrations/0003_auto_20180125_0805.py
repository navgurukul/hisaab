# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-25 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0002_auto_20180123_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
