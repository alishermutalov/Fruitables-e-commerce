# Generated by Django 5.1 on 2024-08-28 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
