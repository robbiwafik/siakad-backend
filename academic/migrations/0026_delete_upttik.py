# Generated by Django 4.1.7 on 2023-03-10 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0025_copy_data_from_upttik_to_tempupttik'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UptTIK',
        ),
    ]
