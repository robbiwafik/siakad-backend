from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Jurusan(models.Model):
    nama = models.CharField(max_length=255)


class Semester(models.Model):
    no = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])


class ProgramPendidikan(models.Model):
    kode = models.CharField(max_length=5, primary_key=True)
    nama = models.CharField(max_length=255)


class GedungKuliah(models.Model):
    nama = models.CharField(max_length=255)


class Pemberitahuan(models.Model):
    judul = models.CharField(max_length=255)
    sub_judul = models.CharField(max_length=255)
    detail = models.TextField(null=True)
    tanggal_terbit = models.DateField(auto_now_add=True)
    tanggal_hapus = models.DateField(null=True)
    thumbnail = models.ImageField()
    file = models.FileField(null=True)
    link = models.URLField(null=True)


class UptTIK(models.Model):
    nip = models.CharField(max_length=20, primary_key=True)
    no_hp = models.CharField(max_length=13)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ProgramStudi(models.Model):
    kode = models.CharField(max_length=10, primary_key=True)
    nama = models.CharField(max_length=255)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT, related_name='prodi_list')
    program_pendidikan = models.ForeignKey(ProgramPendidikan, on_delete=models.PROTECT, related_name='prodi_list')
