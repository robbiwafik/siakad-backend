# Generated by Django 4.1.7 on 2023-03-07 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0018_karyailmiah'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jadwal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kelas', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='jadwal_list', to='academic.kelas')),
            ],
        ),
    ]
