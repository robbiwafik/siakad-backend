from rest_framework import serializers

from . import models


class JurusanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Jurusan
        fields = ['id', 'nama']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semester
        fields = ['no']


class ProgramPendidikanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramPendidikan
        fields = ['kode', 'nama']


class GedungKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GedungKuliah
        fields = ['id', 'nama']


class SimplePemberitahuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pemberitahuan
        fields = ['id', 'judul', 'sub_judul', 'thumbnail']


class PemberitahuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pemberitahuan
        fields = ['id', 'judul', 'sub_judul', 'detail', 'tanggal_terbit', 'thumbnail', 'file', 'link']


class CreateUpdateProgramStudiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramStudi
        fields = ['kode', 'nama', 'jurusan', 'program_pendidikan']


class ProgramStudiSerializer(serializers.ModelSerializer):
    jurusan = JurusanSerializer()
    program_pendidikan = ProgramPendidikanSerializer()
    class Meta:
        model = models.ProgramStudi
        fields = ['kode', 'nama', 'jurusan', 'program_pendidikan']


class StaffProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffProdi
        fields = ['nip', 'nama_depan', 'nama_belakang', 'username', 'email', 'no_hp', 'prodi']


class CreateStaffProdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffProdi
        fields = ['nip', 'no_hp', 'prodi', 'user']


class UpdateStaffProdiSerializer(serializers.ModelSerializer):
    nip = serializers.CharField(max_length=20, read_only=True)
    class Meta:
        model = models.StaffProdi
        fields = ['nip', 'no_hp', 'prodi', 'user']


class CreateUpdateDosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'email', 'no_hp', 'gelar', 'prodi']


class DosenSerializer(serializers.ModelSerializer):
    prodi = ProgramStudiSerializer()
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'email', 'no_hp', 'gelar', 'prodi']


class SimpleDosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dosen
        fields = ['nip', 'nama', 'gelar']


class KelasSerializer(serializers.ModelSerializer):
    prodi = ProgramStudiSerializer()
    class Meta:
        model = models.Kelas
        fields = ['id', 'huruf', 'prodi', 'semester']


class MahasiswaSerializer(serializers.ModelSerializer):
    kelas = KelasSerializer()
    pembimbing_akademik = SimpleDosenSerializer()
    class Meta:
        model = models.Mahasiswa
        fields = ['nim', 'nama_depan', 'nama_belakang', 
                  'email', 'tanggal_lahir', 'alamat', 
                  'no_hp', 'foto_profil', 'pembimbing_akademik', 
                  'kelas']


class CreateUpdateMahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mahasiswa
        fields = ['nim', 'email', 'tanggal_lahir', 
                  'alamat', 'no_hp', 'foto_profil', 
                  'pembimbing_akademik', 'kelas', 'user']


class RuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ruangan
        fields = ['id', 'nama', 'gedung']


class AduanRuanganSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.AduanRuangan.objects.create(ruangan_id=self.context['ruangan_id'], **validated_data)
    class Meta:
        model = models.AduanRuangan
        fields = ['id', 'status', 'detail', 'foto']


class CreateAduanRuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AduanRuangan
        fields = ['id', 'detail', 'foto']


class UpdateAduanRuanganSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AduanRuangan
        fields = ['status']


class PemberitahuanProdiSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return models.PemberitahuanProdi.objects.create(
            pemberitahuan_id=self.context['pemberitahuan_id'],
            **validated_data
        )
    class Meta:
        model = models.PemberitahuanProdi
        fields = ['id', 'prodi']
    
