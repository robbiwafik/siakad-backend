from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Jurusan(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nama

    class Meta:
        verbose_name_plural = 'Jurusan'
    

class Semester(models.Model):
    no = models.PositiveSmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return str(self.no)
    
    class Meta:
        verbose_name_plural = 'Semester'
    

class ProgramPendidikan(models.Model):
    kode = models.CharField(max_length=5, primary_key=True)
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nama

    class Meta:
        verbose_name_plural = 'Program Pendidikan'


class GedungKuliah(models.Model):
    nama = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nama

    class Meta:
        verbose_name_plural = 'Gedung Kuliah'
    

class Pemberitahuan(models.Model):
    judul = models.CharField(max_length=255)
    sub_judul = models.CharField(max_length=255)
    detail = models.TextField(null=True)
    tanggal_terbit = models.DateField(auto_now_add=True)
    tanggal_hapus = models.DateField(null=True)
    thumbnail = models.ImageField(upload_to='academic/images/')
    file = models.FileField(null=True, blank=True, upload_to='academic/files/')
    link = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.judul

    class Meta:
        verbose_name_plural = 'Pemberitahuan'


class UptTIK(models.Model):
    no_induk = models.CharField(max_length=20, unique=True)
    no_hp = models.CharField(max_length=13)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name_plural = 'UPT TIK'


class ProgramStudi(models.Model):
    kode = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=255)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.PROTECT)
    program_pendidikan = models.ForeignKey(ProgramPendidikan, on_delete=models.PROTECT)
    no_sk = models.CharField(max_length=12)
    tanggal_sk = models.DateField()
    tahun_operasional = models.PositiveIntegerField(validators=[MinValueValidator(2000), MaxValueValidator(3000)])
	
    def __str__(self) -> str:
        return self.nama
    
    class Meta:
        verbose_name_plural = 'Program Studi'
    
    
class StaffProdi(models.Model):
    no_induk = models.CharField(max_length=20, unique=True)
    no_hp = models.CharField(max_length=255)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def nama_depan(self):
        return self.user.first_name
    
    def nama_belakang(self):
        return self.user.last_name
    
    def username(self):
        return self.user.username
    
    def email(self):
        return self.user.email
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        verbose_name_plural = 'Staff Prodi'
    

class Dosen(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    no_hp = models.CharField(max_length=13)
    gelar = models.CharField(max_length=20)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.PROTECT)
    foto_profil = models.ImageField(null=True, blank=True, upload_to='academic/images/')

    def __str__(self) -> str:
        return self.nama
    
    class Meta:
        verbose_name_plural = 'Dosen'
    

class Kelas(models.Model):
    huruf = models.CharField(max_length=1)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.PROTECT, related_name='kelas_list')
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT, related_name="kelas_list")

    def __str__(self) -> str:
        return f"{self.prodi} {self.semester} {self.huruf}"
    
    class Meta:
        verbose_name_plural = 'Kelas'


class Mahasiswa(models.Model):
    nim = models.CharField(max_length=10, unique=True)
    tanggal_lahir = models.DateField()
    no_hp = models.CharField(max_length=13, null=True)
    alamat = models.TextField(null=True)
    foto_profil = models.ImageField(null=True)
    tahun_angkatan = models.PositiveIntegerField(validators=[MinValueValidator(2008), MaxValueValidator(3000)])
    pembimbing_akademik = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, related_name='mahasiswa_didik')
    kelas = models.ForeignKey(Kelas, on_delete=models.PROTECT, related_name='mahasiswa_list')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nim

    def nama_depan(self):
        return self.user.first_name
    
    def nama_belakang(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email


class Ruangan(models.Model):
    nama = models.CharField(max_length=255)
    gedung = models.ForeignKey(GedungKuliah, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nama


class AduanRuangan(models.Model):
    STATUS_DI_TANGGAPI = 'D'
    STATUS_BELUM_DIBACA = 'B'
    STATUS_CHOICES = [
        (STATUS_DI_TANGGAPI, 'Di Tanggapi'),
        (STATUS_BELUM_DIBACA, 'Belum Dibaca')
    ]
    detail = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_BELUM_DIBACA)
    foto = models.ImageField()
    ruangan = models.ForeignKey(Ruangan, on_delete=models.CASCADE)


class PemberitahuanProdi(models.Model):
    pemberitahuan = models.ForeignKey(Pemberitahuan, on_delete=models.CASCADE, related_name="filter_prodi")
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.CASCADE, related_name='pemberitahuan_list')


class PemberitahuanJurusan(models.Model):
    pemberitahuan = models.ForeignKey(Pemberitahuan, on_delete=models.CASCADE, related_name='filter_jurusan')
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='pemberitahuan_list')


class KaryaIlmiah(models.Model):
    TIPE_LAPORAN_MAGANG = 'LM'
    TIPE_TUGAS_AKHIR = 'TA'
    TIPE_SKRIPSI = 'S'
    TIPE_PROPOSAL_TA = 'PTA'
    TIPE_PROPOSAL_S = 'PS'
    TIPE_CHOICES = [
        (TIPE_LAPORAN_MAGANG, 'Laporan Magang'),
        (TIPE_TUGAS_AKHIR, 'Tugas Akhir'),
        (TIPE_SKRIPSI, 'Skripsi'),
        (TIPE_PROPOSAL_TA, 'Proposal Tugas Akhir'),
        (TIPE_PROPOSAL_S, 'Proposal Skripsi')
    ]

    judul = models.CharField(max_length=255)
    abstrak = models.TextField(null=True)
    tanggal_terbit = models.DateField(auto_now_add=True)
    link_versi_full = models.URLField(null=True)
    tipe = models.CharField(max_length=3, choices=TIPE_CHOICES)
    file_preview = models.FileField()
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.SET_NULL, null=True, related_name='karya_ilmiah_list')

    # We can get the 'prodi' using 'mahasiswa' field, but the requirement says that this field should be flexible
    # because the 'staff prodi' actor should be able to upload 'karya ilmiah'. 
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.SET_NULL, null=True, related_name='karya_ilmiah_list') # add related_name later


class Jadwal(models.Model):
    kelas = models.OneToOneField(Kelas, on_delete=models.CASCADE, related_name='jadwal_list')


class MataKuliah(models.Model):
    kode = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    jumlah_teori = models.PositiveSmallIntegerField()
    jumlah_pratikum = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.nama


class JadwalMakul(models.Model):
    HARI_SENIN = 'S'
    HARI_SELASA = 'SE'
    HARI_RABU = 'R'
    HARI_KAMIS = 'K'
    HARI_JUMAT = 'J'
    HARI_CHOICES = [
        (HARI_SENIN, 'Senin'),
        (HARI_SELASA, 'Selasa'),
        (HARI_RABU, 'Rabu'),
        (HARI_KAMIS, 'Kamis'),
        (HARI_JUMAT, 'Jumat')
    ]
    
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    hari = models.CharField(max_length=2, choices=HARI_CHOICES, default=HARI_SENIN)
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE, related_name='makul_list')
    dosen = models.ForeignKey(Dosen, on_delete=models.PROTECT, null=True, related_name='makul_ajar') # remove null=True and rename later
    ruangan = models.ForeignKey(Ruangan, on_delete=models.PROTECT)
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['jam_mulai', 'jam_selesai', 'hari', 'ruangan']


class KHS(models.Model):
    ''' 
    Almost all fields defined in this model can be retrieved from the 'mahasiswa' field,
    however the client wants to keep the static version of a 'KHS'. Therefore, the fields that
    can be retrieved from 'mahasiswa' field should be defined individually in the database.
    '''
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    program_studi = models.CharField(max_length=255)
    program_pendidikan = models.CharField(max_length=255)
    tahun_akademik_awal = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(3000)])
    tahun_akademik_akhir = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(3000)])
    dosen_pembimbing = models.CharField(max_length=255)
    kelas = models.CharField(max_length=5)
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='khs_list')
    

class NilaiKHS(models.Model):
    angka_mutu = models.IntegerField(validators=[MaxValueValidator(4)])
    huruf_mutu = models.CharField(max_length=1)
    nilai = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    khs = models.ForeignKey(KHS, on_delete=models.CASCADE, related_name='nilai_list')
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.PROTECT)

    class Meta:
        unique_together = ['mata_kuliah', 'khs']
