# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_customer_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login'),
        ),
    ]
