# Generated by Django 3.1.2 on 2020-12-31 16:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('collaborate', '0019_auto_20201222_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
