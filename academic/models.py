from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Jurusan(models.Model):
    nama = models.CharField(max_length=255)


class Semester(models.Model):
    no = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return str(self.no)
    

class ProgramPendidikan(models.Model):
    kode = models.CharField(max_length=5, primary_key=True)
    nama = models.CharField(max_length=255)


class GedungKuliah(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nama


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

    def __str__(self) -> str:
        return self.nama


class StaffProdi(models.Model):
    nip = models.CharField(max_length=20, primary_key=True)
    no_hp = models.CharField(max_length=255)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE, related_name="staff_prodi_list")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def nama_depan(self):
        return self.user.first_name
    
    def nama_belakang(self):
        return self.user.last_name
    
    def username(self):
        return self.user.username
    
    def email(self):
        return self.user.email
    

class Dosen(models.Model):
    nip = models.CharField(max_length=20, primary_key=True)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    no_hp = models.CharField(max_length=13)
    gelar = models.CharField(max_length=20)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.nama


class Kelas(models.Model):
    huruf = models.CharField(max_length=1)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.PROTECT, related_name="kelas_list")
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, related_name="kelas_list")

    def __str__(self) -> str:
        return self.prodi.kode + str(self.semester.no) + self.huruf


class Mahasiswa(models.Model):
    nim = models.CharField(max_length=10, unique=True)
    tanggal_lahir = models.DateField()
    no_hp = models.CharField(max_length=13, null=True)
    alamat = models.TextField(null=True)
    foto_profil = models.ImageField(null=True)
    pembimbing_akademik = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, related_name='mahasiswa_didik')
    kelas = models.ForeignKey(Kelas, on_delete=models.PROTECT, related_name='mahasiswa_list')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def nama_depan(self):
        return self.user.first_name
    
    def nama_belakang(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email


class Ruangan(models.Model):
    nama = models.CharField(max_length=255)
    gedung = models.ForeignKey(GedungKuliah, on_delete=models.CASCADE)
