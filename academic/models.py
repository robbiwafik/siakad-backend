from django.db import models


class Jurusan(models.Model):
    nama = models.CharField(max_length=255)
