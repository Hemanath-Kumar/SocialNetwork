# Generated by Django 5.1.5 on 2025-02-07 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fullname',
            new_name='Fullname',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='User',
        ),
    ]
