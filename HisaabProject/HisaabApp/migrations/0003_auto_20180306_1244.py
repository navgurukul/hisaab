# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0002_auto_20180304_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyrequest',
            name='type_of_bill',
            field=models.CharField(blank=True, choices=[(b'INTERNET', b'Internet'), (b'ELECTRICITY', b'Electricity'), (3, b'WaterBill'), (4, b'Houserent')], max_length=50, null=True),
        ),
    ]