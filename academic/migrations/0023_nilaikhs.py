# Generated by Django 4.1.7 on 2023-03-08 06:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0022_khs'),
    ]

    operations = [
        migrations.CreateModel(
            name='NilaiKHS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angka_mutu', models.IntegerField(validators=[django.core.validators.MaxValueValidator(4)])),
                ('huruf_mutu', models.CharField(max_length=1)),
                ('nilai', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('khs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nilai_list', to='academic.khs')),
                ('mata_kuliah', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.matakuliah')),
            ],
            options={
                'unique_together': {('mata_kuliah', 'khs')},
            },
        ),
    ]
