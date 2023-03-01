from django.core.validators import MinValueValidator
from django.db import models

class Jurusan(models.Model):
    nama = models.CharField(max_length=255)


class Semester(models.Model):
    no = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])


class ProgramPendidikan(models.Model):
    kode = models.CharField(max_length=5, primary_key=True)
    nama = models.CharField(max_length=255)
    