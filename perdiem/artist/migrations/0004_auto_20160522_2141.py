# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0003_auto_20160522_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='text',
            field=models.TextField(help_text='The content of the update.'),
        ),
    ]
