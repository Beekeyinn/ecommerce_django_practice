# Generated by Django 3.2.7 on 2021-09-30 12:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analytics', '0002_session'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Session',
            new_name='UserSession',
        ),
    ]