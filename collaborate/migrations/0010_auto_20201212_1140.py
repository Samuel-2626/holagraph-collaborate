# Generated by Django 3.1.2 on 2020-12-12 11:40

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collaborate', '0009_auto_20201212_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name'),
        ),
    ]
