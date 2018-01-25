# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-25 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HisaabApp', '0003_auto_20180125_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addexpense',
            name='expense_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='HisaabApp.NgUser'),
        ),
        migrations.AlterField(
            model_name='recordpayment',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_forward', to='HisaabApp.NgUser'),
        ),
        migrations.AlterField(
            model_name='recordpayment',
            name='paid_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_recieved', to='HisaabApp.NgUser'),
        ),
    ]
