# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2023-09-14 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pkeeper_app', '0002_auto_20230914_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests1',
            fields=[
                ('S_id', models.IntegerField(primary_key=True, serialize=False)),
                ('P_address', models.CharField(max_length=255)),
                ('Username', models.CharField(max_length=255)),
                ('Email', models.CharField(max_length=255)),
                ('Password', models.CharField(max_length=255)),
                ('Phone', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Requests',
        ),
        migrations.RemoveField(
            model_name='hospital',
            name='Hospitalname',
        ),
    ]
