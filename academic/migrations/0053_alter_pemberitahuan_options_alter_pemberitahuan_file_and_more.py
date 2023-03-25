# Generated by Django 4.1.7 on 2023-03-22 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0052_alter_gedungkuliah_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pemberitahuan',
            options={'verbose_name_plural': 'Pemberitahuan'},
        ),
        migrations.AlterField(
            model_name='pemberitahuan',
            name='file',
            field=models.FileField(null=True, upload_to='academic/files/'),
        ),
        migrations.AlterField(
            model_name='pemberitahuan',
            name='thumbnail',
            field=models.ImageField(upload_to='academic/images/'),
        ),
    ]
