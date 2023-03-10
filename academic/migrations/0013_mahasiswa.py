# Generated by Django 4.1.7 on 2023-03-03 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0012_kelas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mahasiswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nim', models.CharField(max_length=10, unique=True)),
                ('tanggal_lahir', models.DateField()),
                ('no_hp', models.CharField(max_length=13, null=True)),
                ('alamat', models.TextField(null=True)),
                ('foto_profil', models.ImageField(null=True, upload_to='')),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mahasiswa_list', to='academic.kelas')),
                ('pembimbing_akademik', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mahasiswa_didik', to='academic.dosen')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
