# Generated by Django 5.1.5 on 2025-02-12 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myaccount',
            name='title',
        ),
    ]
