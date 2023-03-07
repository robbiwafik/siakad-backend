from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from . import models, serializers


class JurusanViewSet(ModelViewSet):
    queryset = models.Jurusan.objects.all()
    serializer_class = serializers.JurusanSerializer


class SemesterViewSet(ModelViewSet):
    queryset = models.Semester.objects.all()
    serializer_class = serializers.SemesterSerializer


class ProgramPendidikanViewSet(ModelViewSet):
    queryset = models.ProgramPendidikan.objects.all()
    serializer_class = serializers.ProgramPendidikanSerializer


class GedungKuliahViewSet(ModelViewSet):
    queryset = models.GedungKuliah.objects.all()
    serializer_class = serializers.GedungKuliahSerializer


class PemberitahuanViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'post', 'delete']
    queryset = models.Pemberitahuan.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return serializers.SimplePemberitahuanSerializer
        return serializers.PemberitahuanSerializer


class ProgramStudiViewSet(ModelViewSet):
    queryset = models.ProgramStudi.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateProgramStudiSerializer
        return serializers.ProgramStudiSerializer


class StaffProdiViewSet(ModelViewSet):
    queryset = models.StaffProdi.objects.select_related('user').all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStaffProdiSerializer
        elif self.request.method == 'PUT':
            return serializers.UpdateStaffProdiSerializer
        return serializers.StaffProdiSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateStaffProdiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_prodi = serializer.save()
        serializer = serializers.StaffProdiSerializer(staff_prodi)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DosenViewSet(ModelViewSet):
    queryset = models.Dosen.objects.select_related('prodi').all()
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateDosenSerializer
        return serializers.DosenSerializer


class KelasViewSet(ModelViewSet):
    queryset = models.Kelas.objects\
        .select_related('prodi', 'prodi__jurusan', 'prodi__program_pendidikan', 'semester')\
        .all()
    serializer_class = serializers.KelasSerializer


class MahasiswaViewSet(ModelViewSet):
    queryset = models.Mahasiswa.objects\
        .select_related('pembimbing_akademik', 'kelas', 'kelas__prodi', 'kelas__prodi__jurusan', 'kelas__semester', 'user')\
        .all()
    lookup_field = 'nim'
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateMahasiswaSerializer
        return serializers.MahasiswaSerializer
    

class RuanganViewSet(ModelViewSet):
    queryset = models.Ruangan.objects.all()
    serializer_class = serializers.RuanganSerializer
    

class AduanRuanganViewSet(ModelViewSet):
    def get_queryset(self):
        return models.AduanRuangan.objects.filter(ruangan_id=self.kwargs['ruangan_pk'])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAduanRuanganSerializer
        elif self.request.method == 'PUT':
            return serializers.UpdateAduanRuanganSerializer
        return serializers.AduanRuanganSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ruangan_id'] = self.kwargs['ruangan_pk']
        return context
    

class PemberitahuanProdiViewSet(ModelViewSet):
    serializer_class = serializers.PemberitahuanProdiSerializer

    def get_queryset(self):
        return models.PemberitahuanProdi.objects.filter(pemberitahuan_id=self.kwargs['pemberitahuan_pk'])
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pemberitahuan_id'] = self.kwargs['pemberitahuan_pk']
        return context


class PemberitahuanJurusanViewSet(ModelViewSet):
    serializer_class = serializers.PemberitahuanJurusanSerializer

    def get_queryset(self):
        return models.PemberitahuanJurusan.objects.filter(
            pemberitahuan_id=self.kwargs['pemberitahuan_pk']
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pemberitahuan_id'] = self.kwargs['pemberitahuan_pk']
        return context


class KaryaIlmiahViewSet(ModelViewSet):
    queryset = models.KaryaIlmiah.objects\
        .select_related('prodi', 'prodi__jurusan', 'prodi__program_pendidikan', 'mahasiswa', 'mahasiswa__user')\
        .all()
    serializer_class = serializers.KaryaIlmiahSerializer
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return serializers.CreateUpdateKaryaIlmiahSerializer
        return serializers.KaryaIlmiahSerializer
    