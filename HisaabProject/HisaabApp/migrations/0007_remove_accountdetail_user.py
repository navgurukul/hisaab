# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-31 14:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0006_nguser_has_account_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountdetail',
            name='user',
        ),
    ]
