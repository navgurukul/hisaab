# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0004_auto_20180306_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyrequest',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HisaabApp.Facility'),
        ),
        migrations.AlterField(
            model_name='moneyrequest',
            name='nguser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HisaabApp.NgUser'),
        ),
    ]