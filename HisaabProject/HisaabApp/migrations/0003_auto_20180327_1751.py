# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0002_auto_20180322_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyrequest',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
