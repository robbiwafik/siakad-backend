# Generated by Django 4.1.7 on 2023-03-10 03:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0026_delete_upttik'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TempUptTIK',
            new_name='UptTIK',
        ),
    ]
