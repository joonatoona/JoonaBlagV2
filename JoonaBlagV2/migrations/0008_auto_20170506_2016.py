# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-06 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JoonaBlagV2', '0007_auto_20170506_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128)),
                ('filename', models.CharField(max_length=128)),
                ('content', models.FileField(upload_to='')),
                ('mime', models.CharField(max_length=64)),
            ],
            options={
                'permissions': (('can_upload', 'Can upload files'),),
            },
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('can_post', 'Can post'), ('can_vote_posts', 'Can vote on posts'))},
        ),
    ]