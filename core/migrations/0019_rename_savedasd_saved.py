# Generated by Django 5.1.5 on 2025-03-08 09:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_rename_saved_savedasd'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='savedasd',
            new_name='saved',
        ),
    ]
