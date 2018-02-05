# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-05 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0006_auto_20180205_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashentry',
            name='category',
            field=models.CharField(blank=True, choices=[(b'TRAVEL', b'Travel Expense'), (b'GROCERIES', b'Groceries'), (b'VEGETABLES', b'Vegetables'), (b'HOUSEHOLD', b'HouseholdItems'), (b'EGG', b'Egg'), (b'MILK', b'Milk & Bread'), (b'TECH EXPENCE', b'Tech Expenses'), (b'OTHER', b'Other')], max_length=25, null=True),
        ),
    ]
