# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 16:47
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_text',
            field=tinymce.models.HTMLField(),
        ),
    ]