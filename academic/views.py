from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

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
