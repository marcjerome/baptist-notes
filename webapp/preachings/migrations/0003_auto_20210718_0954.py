# Generated by Django 3.1.4 on 2021-07-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preachings', '0002_preaching_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preaching',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='preachings', to='preachings.Tag'),
        ),
    ]