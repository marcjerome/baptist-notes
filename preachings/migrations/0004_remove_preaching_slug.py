# Generated by Django 3.0.4 on 2020-04-02 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preachings', '0003_preaching_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preaching',
            name='slug',
        ),
    ]
