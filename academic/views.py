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
