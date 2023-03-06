from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('dosen', views.DosenViewSet, basename='dosen')
router.register('gedung', views.GedungKuliahViewSet, basename='gedung')
router.register('jurusan', views.JurusanViewSet, basename='jurusan')
router.register('kelas', views.KelasViewSet, basename='kelas')
router.register('mahasiswa', views.MahasiswaViewSet, basename='mahasiswa')
router.register('pemberitahuan', views.PemberitahuanViewSet, basename='pemberitahuan')
router.register('prodi', views.ProgramStudiViewSet, basename='prodi')
router.register('program_pendidikan', views.ProgramPendidikanViewSet, basename='program_pendidikan')
router.register('ruangan', views.RuanganViewSet, basename='ruangan')
router.register('semester', views.SemesterViewSet, basename='semester')
router.register('staff_prodi', views.StaffProdiViewSet, basename='staff_prodi')

urlpatterns = router.urls
