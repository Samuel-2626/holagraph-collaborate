# Generated by Django 3.1.2 on 2020-12-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborate', '0017_people_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='messagesinchannel',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='room',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]