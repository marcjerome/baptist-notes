# Generated by Django 3.1.4 on 2020-12-03 07:00

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preaching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', ckeditor.fields.RichTextField()),
                ('date', models.DateField()),
                ('slug', models.SlugField(blank=True, editable=False, max_length=265, unique=True)),
                ('privacy', models.BooleanField(default=True)),
                ('tags', models.ManyToManyField(blank=True, related_name='preachings', to='preachings.Tag')),
            ],
        ),
    ]