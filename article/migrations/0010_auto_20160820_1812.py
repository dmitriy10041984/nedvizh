# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-20 18:12
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20160819_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_address',
            field=tinymce.models.HTMLField(default=434, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='article_main_data',
            field=tinymce.models.HTMLField(default=2, verbose_name='Главное о недвижимости'),
            preserve_default=False,
        ),
    ]